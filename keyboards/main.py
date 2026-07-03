from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖥 Статус", callback_data="menu:status"),
                InlineKeyboardButton(text="🎮 Игры", callback_data="menu:gaming"),
            ],
            [
                InlineKeyboardButton(text="📁 Файлы", callback_data="menu:files"),
                InlineKeyboardButton(text="⚡ Питание", callback_data="menu:power"),
            ],
            [
                InlineKeyboardButton(text="🚀 Сценарии", callback_data="menu:scenarios"),
            ],
        ]
    )