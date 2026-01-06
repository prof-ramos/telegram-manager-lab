from pathlib import Path
from typing import Protocol

from telegram_manager.domain.entities.dialog import ScanResult


class DialogExporter(Protocol):
    def export_to_json(self, result: ScanResult, filename: str = "dialogs.json") -> Path:
        ...

    def export_to_csv(self, result: ScanResult, filename: str = "dialogs.csv") -> Path:
        ...
