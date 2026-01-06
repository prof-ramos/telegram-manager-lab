"""
Telegram Manager - Cyber Management Suite

Interface CLI production-grade para gerenciar conversas do Telegram
com estética cyberpunk/synthwave usando Python Rich.

Época: 2026
Versão: 2.0.0 (Refatorado)
Autor: Gabriel Ramos
"""

__version__ = "2.0.0"
__author__ = "Gabriel Ramos"

from .domain.entities.dialog import ScanResult, DialogInfo
from .infrastructure.config.env import TelegramConfig
from .infrastructure.telethon.client import TelegramClientManager
from .infrastructure.telethon.scanner import TelegramScanner

__all__ = [
    'TelegramClientManager',
    'TelegramScanner',
    'ScanResult',
    'DialogInfo',
    'TelegramConfig',
]
