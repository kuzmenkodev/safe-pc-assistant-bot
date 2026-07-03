from __future__ import annotations

from html import escape

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
        await message.answer("<b>🚀 Сценарии</b>\n\nСписок пуст.")
        return

    text = "<b>🚀 Сценарии</b>\n\n" + "\n".join(
        f"• <code>{escape(key)}</code> — {escape(scenario.description)}"
        for key, scenario in scenarios.items()
    )
    text += "\n\nЗапуск: <code>/scenario &lt;имя&gt;</code>"

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
        await message.answer(
            "<b>🚀 Сценарии</b>\n\nИспользование: <code>/scenario &lt;имя&gt;</code>"
        )
        return

    lines = run_scenario(config.data_dir, scenario_key)
    await message.answer("\n".join(lines))