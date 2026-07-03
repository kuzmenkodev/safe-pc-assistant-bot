from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from keyboards.main import main_menu_keyboard
from security.auth import ensure_authorized

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    text = (
        "<b>🖥 ПК-ассистент</b>\n\n"
        "Безопасный Telegram-бот для управления личным ПК.\n"
        "Доступны статус системы, игры, приложения, файлы и сценарии."
    )
    await message.answer(text, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    await message.answer(
        "<b>📖 Команды</b>\n\n"
        "🖥 <code>/status</code> — статус ПК\n"
        "📊 <code>/processes</code> — топ процессов\n"
        "🎮 <code>/gaming</code> — игровой статус\n"
        "📦 <code>/open &lt;имя&gt;</code> — открыть приложение\n"
        "🖥 <code>/runningapps</code> — запущенные приложения\n"
        "📁 <code>/files</code> — разрешённые файлы\n"
        "⚡ <code>/power</code> — действия питания\n"
        "🚀 <code>/scenarios</code> — список сценариев\n"
    )