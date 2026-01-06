import asyncio
import logging
from telethon import types
from telegram_manager.infrastructure.config.env import TelegramConfig
from telegram_manager.infrastructure.telethon.client import TelegramClientManager

# Configure logging only if run directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def check(folder: int = 0) -> None:
    """
    Check for bots in a specific folder.

    Args:
        folder (int): The folder ID to check. Default is 0 (main folder).
    """
    try:
        config = TelegramConfig.from_env()
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return

    try:
        cm = TelegramClientManager(config)
        async with cm.get_client() as client:
            count = 0
            try:
                async for d in client.iter_dialogs(folder=folder):
                    if d.entity and isinstance(d.entity, types.User) and d.entity.bot:
                        count += 1
                logger.info(f"Remaining bots in folder {folder}: {count}")
            except Exception as e:
                logger.error(f"Error iterating dialogs: {e}")

    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Connection error: {e}")
    except Exception as e:
        logger.error(f"Failed to connect to Telegram: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(check())
