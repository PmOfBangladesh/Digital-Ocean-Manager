"""Shared helper utilities for SML Bot."""
from datetime import datetime


DIVIDER = '━' * 20

BOT_TAG = '@codeninjaxd'
BOT_BRAND = 'SML The Unknown'

HEADER = f'<b>🔥 SML Bot</b> | <i>{BOT_BRAND}</i>\n{DIVIDER}\n'


def fmt_header(title: str, emoji: str = '🖥') -> str:
    return f'{emoji} <b>{title}</b>\n{DIVIDER}\n'


def fmt_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
