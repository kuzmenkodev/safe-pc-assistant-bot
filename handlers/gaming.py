from __future__ import annotations

import subprocess

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.gaming_service import get_gaming_snapshot
from services.system_service import get_system_snapshot

router = Router()

ALLOWED_CLOSE = {
    "steam": "steam.exe",
    "discord": "discord.exe",
    "chrome": "chrome.exe",
    "telegram": "telegram.exe",
}


@router.message(Command("gaming"))
async def cmd_gaming(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    gaming = get_gaming_snapshot(config.data_dir)
    system = get_system_snapshot()

    active = ", ".join(gaming.active_items) if gaming.active_items else "ничего не найдено"
    detected = gaming.detected_game or "не найдено"

    await message.answer(
        "<b>🎮 Игровой статус</b>\n\n"
        f"🎯 <b>Игра:</b> <code>{detected}</code>\n"
        f"🧩 <b>Процессы:</b> <code>{active}</code>\n"
        f"🔥 <b>CPU:</b> {system.cpu_percent}%\n"
        f"🧠 <b>RAM:</b> {system.ram_percent}%\n"
        f"🧷 <b>Свободно:</b> {system.free_ram_gb} ГБ"
    )


@router.message(Command("cs2"))
async def cmd_cs2(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    try:
        subprocess.Popen(["cmd", "/c", "start", "", "steam://rungameid/730"], shell=False)
        await message.answer("<b>✅ CS2 запускается</b>\n\nОткрываю игру через Steam.")
    except Exception as e:
        await message.answer(f"<b>❌ Не удалось запустить CS2</b>\n\n{e}")


@router.message(Command("close"))
async def cmd_close(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "<b>⚠️ Не указано приложение</b>\n\n"
            "Пример: <code>/close steam</code>"
        )
        return

    target = parts[1].strip().lower()
    exe_name = ALLOWED_CLOSE.get(target)

    if not exe_name:
        await message.answer(
            "<b>❌ Недоступное приложение</b>\n\n"
            "Можно закрыть: <code>steam</code>, <code>discord</code>, "
            "<code>chrome</code>, <code>telegram</code>"
        )
        return

    try:
        result = subprocess.run(
            ["taskkill", "/f", "/t", "/im", exe_name],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            await message.answer(f"<b>✅ Приложение закрыто</b>\n\nЗакрыл: <code>{target}</code>")
            return

        await message.answer(
            "<b>⚠️ Не удалось закрыть приложение</b>\n\n"
            f"Возможно, <code>{target}</code> сейчас не запущен."
        )
    except Exception as e:
        await message.answer(f"<b>❌ Ошибка закрытия</b>\n\n{e}")


@router.message(Command("shutdown"))
async def cmd_shutdown(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    try:
        subprocess.Popen(["shutdown", "/s", "/t", "10"], shell=False)
        await message.answer("<b>⏻ Выключение ПК</b>\n\nКомпьютер выключится через 10 секунд.")
    except Exception as e:
        await message.answer(f"<b>❌ Ошибка выключения</b>\n\n{e}")


@router.message(Command("restart"))
async def cmd_restart(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    try:
        subprocess.Popen(["shutdown", "/r", "/t", "10"], shell=False)
        await message.answer("<b>🔄 Перезагрузка ПК</b>\n\nКомпьютер перезагрузится через 10 секунд.")
    except Exception as e:
        await message.answer(f"<b>❌ Ошибка перезагрузки</b>\n\n{e}")


@router.message(Command("help"))
async def cmd_help(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    await message.answer(
        "<b>📖 Команды</b>\n\n"
        "🎮 <code>/gaming</code> — игровой статус\n"
        "🎯 <code>/cs2</code> — запустить CS2\n"
        "❌ <code>/close steam</code> — закрыть приложение\n"
        "⏻ <code>/shutdown</code> — выключить ПК\n"
        "🔄 <code>/restart</code> — перезагрузить ПК"
    )