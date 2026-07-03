from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized

router = Router()


@router.message(Command("media"))
async def cmd_media(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    await message.answer(
        "<b>🎵 Медиа</b>\n\n"
        "Пока это заготовка для управления музыкой и звуком.\n"
        "Сюда можно добавить: play/pause, next, previous, volume и mute."
    )