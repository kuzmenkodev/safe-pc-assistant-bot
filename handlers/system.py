from __future__ import annotations

from html import escape

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.system_service import get_system_snapshot, ping_host, top_processes

router = Router()


@router.message(Command("status"))
async def cmd_status(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    snap = get_system_snapshot()

    await message.answer(
        "<b>🖥 Система</b>\n\n"
        f"🔥 <b>CPU:</b> {snap['cpu_percent']:.1f}%\n"
        f"🧠 <b>RAM:</b> {snap['memory_percent']:.1f}%\n"
        f"💿 <b>Disk:</b> {snap['disk_percent']:.1f}%"
    )


@router.message(Command("processes"))
async def cmd_processes(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    rows = top_processes()

    if not rows:
        await message.answer("<b>📊 Процессы</b>\n\nСписок пуст.")
        return

    text = "<b>📊 Топ процессов</b>\n\n" + "\n".join(
        f"• <b>{escape(str(row['name']))}</b> (PID {row['pid']}) — "
        f"CPU {row['cpu_percent']:.1f}% | RAM {row['memory_mb']:.1f} MB"
        for row in rows
    )

    await message.answer(text)


@router.message(Command("ping"))
async def cmd_ping(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    ok, result = ping_host("8.8.8.8")
    prefix = "✅" if ok else "❌"

    await message.answer(
        "<b>🌐 Ping</b>\n\n"
        f"{prefix} {escape(result)}"
    )