from __future__ import annotations

import subprocess
from html import escape

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.gaming_service import get_gaming_snapshot
from services.system_service import get_system_snapshot

router = Router()

ALLOWED_CLOSE: dict[str, str] = {
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

    detected = gaming.detected_game or "не обнаружена"
    active = ", ".join(gaming.active_items) if gaming.active_items else "ничего не найдено"

    await message.answer(
        "<b>🎮 Игры</b>\n\n"
        f"🕹 <b>Текущая игра:</b> {escape(detected)}\n"
        f"🧩 <b>Активно:</b> {escape(active)}\n\n"
        f"🔥 <b>CPU:</b> {system['cpu_percent']:.1f}%\n"
        f"🧠 <b>RAM:</b> {system['memory_percent']:.1f}%\n"
        f"💿 <b>Disk:</b> {system['disk_percent']:.1f}%"
    )


@router.message(Command("cs2"))
async def cmd_cs2(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    try:
        result = subprocess.run(
            ["cmd", "/c", "start", "steam://rungameid/730"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )

        if result.returncode == 0:
            await message.answer("<b>🎯 CS2</b>\n\nЗапуск отправлен в Steam.")
            return

        await message.answer("<b>🎯 CS2</b>\n\nНе удалось запустить игру.")
    except Exception as exc:
        await message.answer(
            f"<b>🎯 CS2</b>\n\n❌ Ошибка запуска: {escape(str(exc))}"
        )


@router.message(Command("close"))
async def cmd_close(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "<b>❌ Закрытие приложения</b>\n\n"
            "Укажи название после команды."
        )
        return

    target = parts[1].strip().lower()
    exe_name = ALLOWED_CLOSE.get(target)

    if not exe_name:
        await message.answer(
            "<b>❌ Закрытие приложения</b>\n\n"
            "Это приложение нельзя закрыть через бота.\n\n"
            "Доступно: <code>steam</code>, <code>discord</code>, "
            "<code>chrome</code>, <code>telegram</code>"
        )
        return

    try:
        result = subprocess.run(
            ["taskkill", "/f", "/t", "/im", exe_name],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )

        if result.returncode == 0:
            await message.answer(f"✅ <b>{escape(target)}</b> закрыто.")
            return

        await message.answer(f"⚠️ <b>{escape(target)}</b> сейчас не запущено.")
    except Exception as exc:
        await message.answer(
            f"❌ Ошибка при закрытии <b>{escape(target)}</b>: {escape(str(exc))}"
        )