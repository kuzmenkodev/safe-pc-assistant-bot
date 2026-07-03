from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_keyboard(key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm:{key}"),
                InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel:{key}"),
            ]
        ]
    )