from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from config import AppConfig
from handlers.power import store
from security.auth import ensure_authorized

router = Router()

MENU_TEXT = {
    "status": "🖥 Используй /status",
    "gaming": "🎮 Используй /gaming",
    "files": "📁 Используй /files",
    "power": "⚡ Используй /power",
    "scenarios": "🚀 Используй /scenarios",
}


@router.callback_query(F.data.startswith("menu:"))
async def menu_callbacks(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    action = callback.data.split(":", 1)[1]

    await callback.answer()
    await callback.message.answer(MENU_TEXT.get(action, "❌ Неизвестное действие."))


@router.callback_query(F.data.startswith("confirm:"))
async def confirm_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    key = callback.data.split(":", 1)[1]
    item = store.get(key)

    if not item:
        await callback.answer("Время подтверждения истекло.", show_alert=True)
        return

    store.delete(key)

    await callback.answer("Подтверждено.")
    await callback.message.answer(f"✅ Действие подтверждено: <code>{item.action}</code>")


@router.callback_query(F.data.startswith("cancel:"))
async def cancel_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    key = callback.data.split(":", 1)[1]
    store.delete(key)

    await callback.answer("Отменено.")
    await callback.message.answer("❌ Действие отменено.")