from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import AppConfig
from security.auth import ensure_authorized
from services.scenarios_service import load_scenarios, run_scenario

router = Router()


@router.message(Command("scenarios"))
async def cmd_scenarios(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    scenarios = load_scenarios(config.data_dir)

    if not scenarios:
        await message.answer("🚀 Сценарии\n\nСписок пуст.")
        return

    text = "🚀 Сценарии\n\n" + "\n".join(
        f"• {key} — {scenario.description}"
        for key, scenario in scenarios.items()
    )
    text += "\n\nЗапуск: /scenario <name>"

    await message.answer(text)


@router.message(Command("scenario"))
async def cmd_scenario(
    message: Message,
    command: CommandObject,
    config: AppConfig,
) -> None:
    if not await ensure_authorized(message, config):
        return

    scenario_key = (command.args or "").strip()

    if not scenario_key:
        await message.answer("Использование: /scenario <name>")
        return

    lines = run_scenario(config.data_dir, scenario_key)
    await message.answer("\n".join(lines))