from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.files_service import list_allowed_files

router = Router()


@router.message(Command("files"))
async def cmd_files(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    items = list_allowed_files(config.data_dir)

    if not items:
        await message.answer("<b>📁 Разрешённые файлы</b>\n\nСписок пуст.")
        return

    text = "<b>📁 Разрешённые файлы</b>\n\n" + "\n".join(
        f"• <code>{item}</code>" for item in items
    )
    await message.answer(text)