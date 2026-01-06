from datetime import datetime
from typing import List, Optional

from telegram_manager.domain.entities.dialog import DialogInfo

from rich.progress import Progress

from telegram_manager.application.ports.media_downloader import MediaDownloader


class DownloadMediaUseCase:
    def __init__(self, downloader: MediaDownloader):
        self.downloader = downloader

    async def execute(
        self,
        dialogs: List[DialogInfo],
        progress: Progress,
        allowed_types: Optional[List[str]] = None,
        min_date: Optional[datetime] = None,
        max_date: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> None:
        await self.downloader.download_all_media(
            dialogs=dialogs,
            progress=progress,
            allowed_types=allowed_types,
            min_date=min_date,
            max_date=max_date,
            limit=limit,
        )
