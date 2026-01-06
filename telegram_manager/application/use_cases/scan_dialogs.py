import logging
from telegram_manager.application.ports.dialog_scanner import DialogScanner
from telegram_manager.domain.entities.dialog import ScanResult


class ScanDialogsUseCase:
    """
    Orchestrates the dialog scanning process using a provided DialogScanner.
    Responsible for initiating the scan and returning the result.
    """

    def __init__(self, scanner: DialogScanner):
        self.scanner = scanner
        self.logger = logging.getLogger(__name__)

    async def execute(self) -> ScanResult:
        """
        Executes the scan process.

        Returns:
            ScanResult: The result of the scan.

        Raises:
            Exception: If the scan fails, errors are logged and re-raised (or could return empty result depending on policy).
                       Currently logging and re-raising to let CLI handle it.
        """
        self.logger.info("Starting dialog scan...")
        try:
            result = await self.scanner.scan_all_dialogs()
            self.logger.info(f"Scan completed. Found {result.total} dialogs.")
            return result
        except Exception as e:
            self.logger.error(f"Scan failed: {e}", exc_info=True)
            raise
