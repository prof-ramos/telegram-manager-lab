from telegram_manager.infrastructure.config.env import TelegramConfig
from pathlib import Path
import os
from unittest.mock import patch


def test_config_defaults():
    """Verify default values for configuration."""
    with patch.dict(
        os.environ,
        {
            "TELEGRAM_API_ID": "12345",
            "TELEGRAM_API_HASH": "abcdef1234567890abcdef1234567890",
            "TELEGRAM_PHONE": "+1234567890",
        },
    ):
        config = TelegramConfig.from_env()
        assert config.download_dir == Path("downloads")
        assert config.backup_dir == Path("backups")


def test_config_custom_paths():
    """Verify custom paths from environment variables."""
    with patch.dict(
        os.environ,
        {
            "TELEGRAM_API_ID": "12345",
            "TELEGRAM_API_HASH": "abcdef1234567890abcdef1234567890",
            "TELEGRAM_PHONE": "+1234567890",
            "DOWNLOAD_DIR": "custom_downloads",
            "BACKUP_DIR": "custom_backups",
        },
    ):
        config = TelegramConfig.from_env()
        assert config.download_dir == Path("custom_downloads")
        assert config.backup_dir == Path("custom_backups")
