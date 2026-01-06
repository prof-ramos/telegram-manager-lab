import json
import csv
from pathlib import Path
from typing import List
import logging
from telegram_manager.domain.entities.dialog import ScanResult, DialogInfo

logger = logging.getLogger(__name__)


class DialogExporter:
    def __init__(self, output_dir: Path = Path("exports")):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def export_to_json(self, result: ScanResult, filename: str = "dialogs.json") -> Path:
        try:
            data = {
                'stats': result.stats,
                'users': [self._dialog_to_dict(d) for d in result.users],
                'bots': [self._dialog_to_dict(d) for d in result.bots],
                'groups': [self._dialog_to_dict(d) for d in result.groups],
                'channels': [self._dialog_to_dict(d) for d in result.channels],
            }
            
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Dados exportados para JSON: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erro ao exportar JSON: {e}")
            raise
    
    def export_to_csv(self, result: ScanResult, filename: str = "dialogs.csv") -> Path:
        try:
            filepath = self.output_dir / filename
            all_dialogs = result.users + result.bots + result.groups + result.channels
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'name', 'type', 'username', 'participants_count', 'is_official'])
                writer.writeheader()
                
                for dialog in all_dialogs:
                    writer.writerow(self._dialog_to_dict(dialog))
            
            logger.info(f"Dados exportados para CSV: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {e}")
            raise
    
    @staticmethod
    def _dialog_to_dict(dialog: DialogInfo) -> dict:
        return {
            'id': dialog.id,
            'name': dialog.name,
            'type': dialog.type,
            'username': dialog.username,
            'participants_count': dialog.participants_count,
            'is_official': dialog.is_official
        }
