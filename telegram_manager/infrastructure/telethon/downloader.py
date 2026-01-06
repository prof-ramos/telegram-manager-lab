import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Set

import aiofiles
from rich.progress import Progress, TaskID
from telethon import TelegramClient

logger = logging.getLogger(__name__)


class MediaDownloader:
    def __init__(self, client: TelegramClient, base_path: str = "downloads"):
        self.client = client
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        # Limit concurrent downloads to prevent FloodWait and bandwidth saturation
        self.semaphore = asyncio.Semaphore(6)

    async def download_all_media(
        self,
        dialogs: List,
        progress: Progress,
        allowed_types: List[str] = None,
        min_date: datetime = None,
        max_date: datetime = None,
        limit: int = None,
    ) -> None:
        """
        Downloads media from a list of dialogs with optional filters.
        Uses a Worker Pool to process multiple chats in parallel.
        """
        overall_task = progress.add_task(
            f"Processing {len(dialogs)} chats...", total=len(dialogs)
        )

        # Queue of dialogs to process
        queue = asyncio.Queue()
        for dialog in dialogs:
            queue.put_nowait(dialog)

        # Worker function
        async def worker():
            while not queue.empty():
                try:
                    # Non-blocking get
                    current_dialog = queue.get_nowait()
                except asyncio.QueueEmpty:
                    break

                try:
                    await self.process_dialog(
                        current_dialog,
                        progress,
                        allowed_types,
                        min_date,
                        max_date,
                        limit,
                    )
                except Exception as e:
                    logger.error(f"Error in worker for {current_dialog.name}: {e}")
                finally:
                    progress.advance(overall_task)
                    # queue.task_done() # Removed as queue.join() is not used

        # Start workers (e.g., 3 parallel chats)
        # The internal self.semaphore will still limit total global file downloads.
        NUM_WORKERS = 3
        workers = [asyncio.create_task(worker()) for _ in range(NUM_WORKERS)]

        await asyncio.gather(*workers)

    async def process_dialog(
        self,
        dialog_info,
        progress: Progress,
        allowed_types: List[str] = None,
        min_date: datetime = None,
        max_date: datetime = None,
        limit: int = None,
    ) -> None:
        """
        Downloads media from a single dialog with filters.
        """
        # Create chat directory: Type/SafeName_ID
        safe_name = (
            "".join(c for c in dialog_info.name if c.isalnum() or c in (" ", "_", "-"))
            .strip()
            .replace(" ", "_")
        )
        if not safe_name:
            safe_name = "unnamed"

        # Organize by type (Users, Groups, etc.)
        type_dir = self.base_path / dialog_info.type
        type_dir.mkdir(exist_ok=True)

        folder_name = f"{safe_name}_{dialog_info.id}"
        chat_path = type_dir / folder_name
        chat_path.mkdir(exist_ok=True)

        # Text history file
        history_path = chat_path / "chat_history.txt"

        # We need to get the entity to iterate messages
        try:
            entity = await self.client.get_entity(dialog_info.id)
        except Exception as e:
            logger.error(
                f"Could not get entity for {dialog_info.name} ({dialog_info.id}): {e}"
            )
            return

        chat_task = progress.add_task(f"Scanning {dialog_info.name}...", total=None)

        # Concurrent Task Management
        active_tasks: Set[asyncio.Task] = set()
        MAX_BUFFER_SIZE = 50  # Increased buffer for better throughput

        try:
            # Use async file handling inside loop
            # Iterate messages
            # Note: reverse=True iterates oldest to newest. Telethon limits apply to total fetched.

            # Precompute UTC dates for comparison
            min_date_utc = min_date.astimezone(timezone.utc) if min_date else None
            max_date_utc = max_date.astimezone(timezone.utc) if max_date else None

            # Open history file once
            async with aiofiles.open(
                history_path, "a", encoding="utf-8"
            ) as history_file:
                async for message in self.client.iter_messages(
                    entity, reverse=True, limit=limit
                ):
                    # Date Filter - Ensure UTC comparison
                    if min_date_utc or max_date_utc:
                        message_date = message.date.astimezone(timezone.utc)
                        if min_date_utc and message_date < min_date_utc:
                            continue
                        if max_date_utc and message_date > max_date_utc:
                            continue

                    # 1. Export Text
                    if message.text:
                        timestamp = message.date.strftime("%Y-%m-%d %H:%M:%S")

                        sender = "Unknown"
                        if message.sender:
                            sender = getattr(
                                message.sender, "username", None
                            ) or getattr(message.sender, "first_name", "Unknown")

                        await history_file.write(
                            f"[{timestamp}] {sender}: {message.text}\n"
                        )
                        await history_file.write("-" * 40 + "\n")

                # 2. Download Media (Concurrent)
                if message.media and self._should_download_media(
                    message, allowed_types
                ):
                    # Create task
                    task = asyncio.create_task(
                        self._download_wrapper(message, chat_path, progress, chat_task)
                    )
                    active_tasks.add(task)
                    task.add_done_callback(active_tasks.discard)

                    # Throttle if too many active tasks
                    if len(active_tasks) >= MAX_BUFFER_SIZE:
                        # Wait for at least one to finish
                        await asyncio.wait(
                            active_tasks, return_when=asyncio.FIRST_COMPLETED
                        )

            # Wait for remaining tasks
            if active_tasks:
                await asyncio.wait(active_tasks)

        except Exception as e:
            logger.error(f"Error processing chat {dialog_info.name}: {e}")
        finally:
            # Clean up any remaining tasks
            if active_tasks:
                for task in active_tasks:
                    task.cancel()
                await asyncio.gather(*active_tasks, return_exceptions=True)
            progress.remove_task(chat_task)

    def _should_download_media(self, message, allowed_types: List[str]) -> bool:
        """Check if message media matches allowed types."""
        if not allowed_types or "all" in allowed_types:
            return True

        if "photo" in allowed_types and message.photo:
            return True
        if "video" in allowed_types and message.video:
            return True
        if "voice" in allowed_types and message.voice:
            return True
        if "audio" in allowed_types and message.audio:
            return True

        if "document" in allowed_types and message.document:
            # If strictly looking for documents (and not just any media that happens to be a document)
            # we might want to exclude things that are also video/audio etc.
            # checking message.file.name extension or mime type effectively.
            # For now, if it's a document and not explicitly another type we already caught, return True
            if not (message.photo or message.video or message.voice or message.audio):
                return True

        return False

    async def _download_wrapper(self, message, chat_path, progress, task_id):
        """Wrapper to respect semaphore."""
        async with self.semaphore:
            await self._download_message_media(message, chat_path, progress, task_id)

    async def _download_message_media(
        self, message, chat_path: Path, progress: Progress, task_id: TaskID
    ) -> None:
        """
        Helper to download media from a single message.
        """
        try:
            # Generate prefix: YYYYMMDD_HHMMSS_MSGID
            date_str = message.date.strftime("%Y%m%d_%H%M%S")
            prefix = f"{date_str}_{message.id}"

            # Determine extension
            ext = getattr(message.file, "ext", "") if message.file else ""

            # Use original filename if available, otherwise use message id
            orig_filename = getattr(message.file, "name", f"{message.id}{ext}")
            if not orig_filename:  # fallback
                orig_filename = f"{message.id}{ext}"

            new_filename = f"{prefix}_{orig_filename}"
            final_path = chat_path / new_filename

            # Check if file already exists
            if final_path.exists():
                return

            # Helper callback for download progress
            download_task = None

            def progress_callback(current, total):
                nonlocal download_task
                if download_task is None:
                    download_task = progress.add_task(
                        f"Downloading {message.id}...", total=total
                    )
                progress.update(download_task, completed=current)

            # Update status
            progress.update(
                task_id, description=f"Downloading media in {chat_path.name}..."
            )

            try:
                # Download directly to final path
                await self.client.download_media(
                    message, file=final_path, progress_callback=progress_callback
                )
            finally:
                if download_task:
                    progress.remove_task(download_task)

        except Exception as e:
            logger.error(f"Failed to download media for message {message.id}: {e}")
