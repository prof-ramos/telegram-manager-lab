import asyncio
from contextlib import asynccontextmanager
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
import logging
from typing import AsyncGenerator
from pathlib import Path

logger = logging.getLogger(__name__)


class TelegramClientManager:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.session_file = Path(config.session_name)
    
    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[TelegramClient, None]:
        self.client = TelegramClient(
            str(self.session_file),
            int(self.config.api_id),
            self.config.api_hash
        )
        
        try:
            if not self.client.is_connected():
                await self.client.connect()
            
            if not await self.client.is_user_authorized():
                await self.client.start(phone=self.config.phone)
            
            logger.info("Cliente Telegram conectado com sucesso")
            yield self.client
            
        except SessionPasswordNeededError:
            logger.error("Senha de 2FA necessaria")
            raise
        except FloodWaitError as e:
            logger.warning(f"FloodWait detectado: aguarde {e.seconds}s")
            raise
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            raise
        finally:
            if self.client:
                await self.client.disconnect()
                logger.info("Cliente Telegram desconectado")
