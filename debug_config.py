from telegram_manager.infrastructure.config.env import TelegramConfig
from pathlib import Path
import os

# Mock env vars
os.environ["TELEGRAM_API_ID"] = "123"
os.environ["TELEGRAM_API_HASH"] = "abc" * 10 + "12"
os.environ["TELEGRAM_PHONE"] = "+1234567890"

try:
    config = TelegramConfig.from_env()
    print(f"Config created: {config}")
    print(f"Has download_dir: {hasattr(config, 'download_dir')}")
    print(f"download_dir value: {config.download_dir}")
except Exception as e:
    print(f"Error: {e}")
