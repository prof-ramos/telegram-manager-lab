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

from .core.client import TelegramClientManager
from .core.scanner import TelegramScanner, ScanResult, DialogInfo
from .utils.config import TelegramConfig

__all__ = [
    'TelegramClientManager',
    'TelegramScanner',
    'ScanResult',
    'DialogInfo',
    'TelegramConfig',
]
