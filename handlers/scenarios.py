from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.scenarios_service import load_scenarios

router = Router()


@router.message(Command("scenarios"))
async def cmd_scenarios(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    scenarios = load_scenarios(config.data_dir)

    if not scenarios:
        await message.answer("<b>🚀 Сценарии</b>\n\nСписок пуст.")
        return

    text = "<b>🚀 Сценарии</b>\n\n" + "\n".join(
        f"• <code>{key}</code> — {scenario.description}"
        for key, scenario in scenarios.items()
    )
    await message.answer(text)