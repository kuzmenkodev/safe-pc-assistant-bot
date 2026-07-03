from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.system_service import get_system_snapshot, top_processes

router = Router()


@router.message(Command("status"))
async def cmd_status(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    snap = get_system_snapshot()

    text = (
        "<b>🖥 Статус ПК</b>\n\n"
        f"🧠 <b>Хост:</b> <code>{snap.hostname}</code>\n"
        f"💿 <b>Система:</b> {snap.os_name}\n"
        f"⏱ <b>Время работы:</b> {snap.uptime_hours} ч\n"
        f"🔥 <b>CPU:</b> {snap.cpu_percent}%\n"
        f"🧷 <b>RAM:</b> {snap.ram_percent}% (свободно {snap.free_ram_gb} ГБ)\n"
        f"📀 <b>Диск:</b> {snap.disk_percent}%\n"
        f"🌐 <b>Локальный IP:</b> <code>{snap.local_ip}</code>"
    )
    await message.answer(text)


@router.message(Command("processes"))
async def cmd_processes(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    rows = top_processes()

    if not rows:
        await message.answer("<b>📊 Процессы</b>\n\nСписок пуст.")
        return

    text = "<b>📊 Топ процессов</b>\n\n" + "\n".join(
        f"• {name}: CPU {cpu:.1f}% | RAM {mem:.1f}%"
        for name, cpu, mem in rows
    )
    await message.answer(text)