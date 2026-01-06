from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


@dataclass
class TelegramConfig:
    api_id: str
    api_hash: str
    phone: str
    session_name: str = "telegram_manager"
    backup_dir: Path = Path("backups")
    download_dir: Path = Path("downloads")
    log_level: str = "INFO"

    @classmethod
    def from_env(cls):
        load_dotenv()

        api_id = os.getenv("TELEGRAM_API_ID")
        api_hash = os.getenv("TELEGRAM_API_HASH")
        phone = os.getenv("TELEGRAM_PHONE")
        session_name = os.getenv("SESSION_NAME", "telegram_manager")
        backup_dir = Path(os.getenv("BACKUP_DIR", "backups"))
        download_dir = Path(os.getenv("DOWNLOAD_DIR", "downloads"))
        log_level = os.getenv("LOG_LEVEL", "INFO")

        if not all([api_id, api_hash, phone]):
            raise ValueError(
                "Variaveis de ambiente obrigatorias nao encontradas!\n"
                "TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE"
            )

        backup_dir.mkdir(exist_ok=True, parents=True)
        download_dir.mkdir(exist_ok=True, parents=True)

        return cls(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            session_name=session_name,
            backup_dir=backup_dir,
            download_dir=download_dir,
            log_level=log_level,
        )

    def validate(self) -> bool:
        try:
            if not self.api_id.isdigit():
                logger.error("API ID deve conter apenas numeros")
                return False

            if len(self.api_hash) != 32:
                logger.error("API Hash deve ter exatamente 32 caracteres")
                return False

            if not self.phone.startswith("+"):
                logger.error("Telefone deve comecar com '+'")
                return False

            return True
        except Exception as e:
            logger.error(f"Erro ao validar configuracoes: {e}")
            return False
