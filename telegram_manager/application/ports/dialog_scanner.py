from typing import Protocol

from telegram_manager.domain.entities.dialog import ScanResult


class DialogScanner(Protocol):
    """
    Protocol describing a scanner responsible for fetching all available dialogs/conversations.
    Implementations should handle connection details and return a standardized ScanResult.
    """

    async def scan_all_dialogs(self) -> ScanResult:
        """
        Scans all dialogs available to the client.

        Returns:
            ScanResult: Object containing lists of users, bots, groups, and channels found,
                        along with metadata like timestamp and total counts.

        befores:
            Raises specific errors (ConnectionError, etc.) if scanning fails.
        """
        ...
