from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel
import logging

from telegram_manager.domain.entities.dialog import DialogInfo, ScanResult
from telegram_manager.domain.policies.bot_classification import is_official_bot

logger = logging.getLogger(__name__)


class TelegramScanner:
    def __init__(self, client: TelegramClient):
        self.client = client
    
    async def scan_all_dialogs(self) -> ScanResult:
        result = ScanResult()
        
        try:
            async for dialog in self.client.iter_dialogs():
                entity = dialog.entity
                dialog_info = await self._create_dialog_info(entity)
                
                if isinstance(entity, User):
                    if entity.bot:
                        result.bots.append(dialog_info)
                    else:
                        result.users.append(dialog_info)
                elif isinstance(entity, Chat):
                    result.groups.append(dialog_info)
                elif isinstance(entity, Channel):
                    if entity.broadcast:
                        result.channels.append(dialog_info)
                    else:
                        result.groups.append(dialog_info)
            
            logger.info(f"Escaneamento concluido: {result.total} dialogos encontrados")
        except Exception as e:
            logger.error(f"Erro ao escanear dialogos: {e}")
            raise
        
        return result
    
    async def _create_dialog_info(self, entity) -> DialogInfo:
        name = getattr(entity, 'title', None) or getattr(entity, 'username', None) or "Unnamed"
        username = getattr(entity, 'username', '')
        is_official = (
            is_official_bot(username) if isinstance(entity, User) and entity.bot else False
        )
        
        participants_count = 0
        if hasattr(entity, 'participants_count'):
            participants_count = entity.participants_count or 0
        
        return DialogInfo(
            id=entity.id,
            name=name,
            type=type(entity).__name__,
            is_official=is_official,
            username=username,
            participants_count=participants_count
        )
