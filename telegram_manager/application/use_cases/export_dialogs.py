from dataclasses import dataclass
from pathlib import Path

from telegram_manager.application.ports.dialog_exporter import DialogExporter
from telegram_manager.domain.entities.dialog import ScanResult


@dataclass(frozen=True)
class ExportedPaths:
    json_path: Path
    csv_path: Path


class ExportDialogsUseCase:
    def __init__(self, exporter: DialogExporter):
        self.exporter = exporter

    def execute(self, result: ScanResult) -> ExportedPaths:
        json_path = self.exporter.export_to_json(result)
        csv_path = self.exporter.export_to_csv(result)
        return ExportedPaths(json_path=json_path, csv_path=csv_path)
