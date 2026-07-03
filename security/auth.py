from __future__ import annotations

from aiogram.types import CallbackQuery, Message

from config import AppConfig


def is_authorized(config: AppConfig, user_id: int | None, chat_id: int | None) -> bool:
    if user_id is None:
        return False
    user_ok = not config.authorized_user_ids or user_id in config.authorized_user_ids
    chat_ok = not config.authorized_chat_ids or (chat_id is not None and chat_id in config.authorized_chat_ids)
    return user_ok and chat_ok


async def ensure_authorized(event: Message | CallbackQuery, config: AppConfig) -> bool:
    user_id = event.from_user.id if event.from_user else None
    if isinstance(event, CallbackQuery):
        chat_id = event.message.chat.id if event.message else None
    else:
        chat_id = event.chat.id
    if is_authorized(config, user_id, chat_id):
        return True
    if isinstance(event, CallbackQuery):
        await event.answer('⛔ Access denied', show_alert=True)
    else:
        await event.answer('⛔ Access denied.')
    return False
