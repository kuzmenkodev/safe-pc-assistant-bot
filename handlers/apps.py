from __future__ import annotations

from html import escape

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.apps_service import load_apps, open_allowed_app, running_allowlisted_apps

router = Router()


@router.message(Command("apps"))
async def cmd_apps(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    apps = load_apps(config.data_dir)

    if not apps:
        await message.answer("<b>📦 Приложения</b>\n\nСписок пуст.")
        return

    text = "<b>📦 Доступные приложения</b>\n\n" + "\n".join(
        f"• <code>{escape(key)}</code> — {escape(app.display_name)}"
        for key, app in apps.items()
    )

    await message.answer(text)


@router.message(Command("open"))
async def cmd_open(
    message: Message,
    command: CommandObject,
    config: AppConfig,
) -> None:
    if not await ensure_authorized(message, config):
        return

    app_key = (command.args or "").strip().lower()

    if not app_key:
        await message.answer(
            "<b>📦 Открытие приложения</b>\n\n"
            "Укажи имя приложения после команды.\n\n"
            "Пример: <code>/open steam</code>"
        )
        return

    ok, result = open_allowed_app(config.data_dir, app_key)
    prefix = "✅" if ok else "❌"

    await message.answer(
        "<b>📦 Открытие приложения</b>\n\n"
        f"{prefix} {escape(result)}"
    )


@router.message(Command("runningapps"))
async def cmd_runningapps(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    items = running_allowlisted_apps(config.data_dir)

    if not items:
        await message.answer("<b>🖥 Запущенные приложения</b>\n\nНичего не найдено.")
        return

    text = "<b>🖥 Запущенные приложения</b>\n\n" + "\n".join(
        f"• {escape(item)}" for item in items
    )

    await message.answer(text)