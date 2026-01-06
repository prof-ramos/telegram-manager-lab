from dataclasses import dataclass

from telegram_manager.application.use_cases.download_media import DownloadMediaUseCase
from telegram_manager.application.use_cases.export_dialogs import ExportDialogsUseCase
from telegram_manager.application.use_cases.scan_dialogs import ScanDialogsUseCase
from telegram_manager.infrastructure.config.env import TelegramConfig
from telegram_manager.infrastructure.storage.dialog_exporter import DialogExporter
from telegram_manager.infrastructure.telethon.client import TelegramClientManager
from telegram_manager.infrastructure.telethon.downloader import MediaDownloader
from telegram_manager.infrastructure.telethon.scanner import TelegramScanner


@dataclass
class AppContainer:
    config: TelegramConfig
    client_manager: TelegramClientManager
    exporter: DialogExporter

    _scanner: TelegramScanner | None = None
    _downloader: MediaDownloader | None = None

    def scan_use_case(self, client) -> ScanDialogsUseCase:
        # Note: 'client' should strictly be typed, but we'll leave it dynamic or import it if safe.
        # Ideally: from telethon import TelegramClient or our wrapper
        if not self._scanner:
            self._scanner = TelegramScanner(client)
        return ScanDialogsUseCase(self._scanner)

    def export_use_case(self) -> ExportDialogsUseCase:
        return ExportDialogsUseCase(self.exporter)

    def download_use_case(self, client) -> DownloadMediaUseCase:
        if not self._downloader:
            self._downloader = MediaDownloader(client)
        return DownloadMediaUseCase(self._downloader)


def build_app() -> AppContainer:
    config = TelegramConfig.from_env()
    client_manager = TelegramClientManager(config)
    exporter = DialogExporter()
    return AppContainer(config=config, client_manager=client_manager, exporter=exporter)
