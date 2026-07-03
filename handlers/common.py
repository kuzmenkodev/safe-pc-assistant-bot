from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import AppConfig
from keyboards.main import main_menu_keyboard
from security.auth import ensure_authorized

router = Router()

GITHUB_URL = "https://github.com/kuzmenkodev/safe-pc-assistant-bot"


def help_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 GitHub", url=GITHUB_URL)],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main")],
        ]
    )


@router.message(Command("start"))
async def cmd_start(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    await message.answer(
        "<b>🤖 PC Assistant Bot</b>\n\n"
        "Быстрый доступ к основным функциям этого ПК.\n\n"
        "Здесь можно открыть приложения, проверить систему, "
        "запустить сценарии и использовать другие готовые действия.\n\n"
        "Выбери раздел ниже.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    await message.answer(
        "<b>ℹ️ О боте</b>\n\n"
        "Это личный бот для удобного и безопасного управления этим ПК.\n"
        "Он работает только с заранее разрешёнными действиями и не даёт полный удалённый доступ.\n\n"
        "Через него можно смотреть состояние системы, открывать приложения, "
        "проверять игровой статус, запускать сценарии и подтверждать действия питания.\n\n"
        "Основная навигация находится в меню ниже.",
        reply_markup=help_keyboard(),
    )
    )