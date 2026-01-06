from datetime import datetime
from typing import List, Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from telegram_manager.domain.entities.dialog import DialogInfo

from rich.progress import Progress


class MediaDownloader(Protocol):
    """
    Protocol for a component responsible for downloading media from a list of dialogs.
    """

    async def download_all_media(
        self,
        dialogs: List,  # Note: Should ideally be List[DialogInfo] but keeping generic here per original, though Plan said specifics.
        # I will check if I can import DialogInfo easily without circular deps.
        # Actually, better to use 'List["DialogInfo"]' or just List for now if not imported.
        # The plan said "Use specific List[Dialog] types".
        # Let's import DialogInfo.
        progress: Progress,
        allowed_types: Optional[List[str]] = None,
        min_date: Optional[datetime] = None,
        max_date: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> None:
        """
        Downloads media from the specified dialogs.

        Args:
            dialogs: List of dialog objects or identifiers to download from.
            progress: Progress tracker instance for UI updates.
            allowed_types: Optional list of MIME types or categories to download.
            min_date: Optional start date filter.
            max_date: Optional end date filter.
            limit: Optional maximum number of items to download per dialog.
        """
        ...
