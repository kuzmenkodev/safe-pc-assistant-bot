from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.apps_service import load_apps, open_allowed_app, running_allowlisted_apps

router = Router()


@router.message(Command("open"))
async def cmd_open(message: Message, command: CommandObject, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    if not command.args:
        apps = load_apps(config.data_dir)

        if not apps:
            await message.answer("<b>📦 Приложения</b>\n\nСписок пуст.")
            return

        text = "<b>📦 Приложения</b>\n\n" + "\n".join(
            f"• <code>{key}</code> — {app.display_name}"
            for key, app in apps.items()
        )
        text += "\n\n🚀 <code>/open chrome</code>\n🖥 <code>/runningapps</code>"

        await message.answer(text)
        return

    app_key = command.args.strip().lower()
    ok, result = open_allowed_app(config.data_dir, app_key)

    if ok:
        await message.answer(f"<b>✅ Приложение запущено</b>\n\n<code>{app_key}</code>")
        return

    await message.answer(f"<b>❌ Не удалось запустить приложение</b>\n\n{result}")


@router.message(Command("runningapps"))
async def cmd_runningapps(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    apps = running_allowlisted_apps(config.data_dir)

    if not apps:
        await message.answer("<b>🖥 Запущенные приложения</b>\n\nСписок пуст.")
        return

    text = "<b>🖥 Запущенные приложения</b>\n\n" + "\n".join(
        f"• <code>{app}</code>" for app in apps
    )
    text += f"\n\n<b>Всего:</b> {len(apps)}"

    await message.answer(text)