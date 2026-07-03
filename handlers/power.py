from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import AppConfig
from keyboards.confirmations import confirm_keyboard
from security.auth import ensure_authorized
from security.confirmations import ConfirmationStore

router = Router()
store = ConfirmationStore(ttl_seconds=30)


@router.message(Command("power"))
async def cmd_power(message: Message, config: AppConfig) -> None:
    if not await ensure_authorized(message, config):
        return

    user_id = message.from_user.id
    key = f"{user_id}:shutdown"

    store.create(
        key=key,
        user_id=user_id,
        action="shutdown",
        payload="shutdown",
    )

    await message.answer(
        "<b>⚡ Питание</b>\n\n"
        "Выключение ПК нужно подтвердить.\n\n"
        "Нажми кнопку ниже, чтобы продолжить.",
        reply_markup=confirm_keyboard(key),
        parse_mode="HTML",
    )