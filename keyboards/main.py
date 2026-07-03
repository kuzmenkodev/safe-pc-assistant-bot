from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖥 Система", callback_data="menu:system"),
                InlineKeyboardButton(text="🎮 Игры", callback_data="menu:gaming"),
            ],
            [
                InlineKeyboardButton(text="📦 Приложения", callback_data="menu:apps"),
                InlineKeyboardButton(text="🚀 Сценарии", callback_data="menu:scenarios"),
            ],
            [
                InlineKeyboardButton(text="📁 Файлы", callback_data="menu:files"),
                InlineKeyboardButton(text="🎵 Медиа", callback_data="menu:media"),
            ],
            [
                InlineKeyboardButton(text="⚡ Питание", callback_data="menu:power"),
                InlineKeyboardButton(text="ℹ️ О боте", callback_data="menu:help"),
            ],
        ]
    )