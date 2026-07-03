from __future__ import annotations

from html import escape

from aiogram import F, Router
from aiogram.types import CallbackQuery

from config import AppConfig
from keyboards.catalogs import (
    apps_keyboard,
    media_keyboard,
    scenarios_keyboard,
    system_keyboard,
)
from keyboards.main import main_menu_keyboard
from security.auth import ensure_authorized
from security.confirmations import ConfirmationStore
from services.apps_service import load_apps, open_allowed_app
from services.files_service import list_allowed_files
from services.gaming_service import get_gaming_snapshot
from services.scenarios_service import load_scenarios, run_scenario
from services.system_service import (
    get_system_snapshot,
    mute_volume,
    ping_host,
    set_volume,
    shutdown_pc,
    top_processes,
)

router = Router()
store = ConfirmationStore(ttl_seconds=30)


@router.callback_query(F.data.startswith("menu:"))
async def menu_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    action = callback.data.split(":", 1)[1]

    if action in {"main", "root"}:
        await callback.message.answer(
            "<b>📋 Главное меню</b>\n\nВыбери раздел ниже.",
            reply_markup=main_menu_keyboard(),
        )

    elif action == "system":
        await callback.message.answer(
            "<b>🖥 Система</b>\n\nВыбери действие.",
            reply_markup=system_keyboard(),
        )

    elif action == "apps":
        apps = load_apps(config.data_dir)
        if not apps:
            await callback.message.answer("<b>📦 Приложения</b>\n\nСписок пуст.")
        else:
            await callback.message.answer(
                "<b>📦 Приложения</b>\n\nВыбери приложение.",
                reply_markup=apps_keyboard(apps),
            )

    elif action == "scenarios":
        scenarios = load_scenarios(config.data_dir)
        if not scenarios:
            await callback.message.answer("<b>🚀 Сценарии</b>\n\nСписок пуст.")
        else:
            await callback.message.answer(
                "<b>🚀 Сценарии</b>\n\nВыбери сценарий.",
                reply_markup=scenarios_keyboard(scenarios),
            )

    elif action == "gaming":
        snap = get_gaming_snapshot(config.data_dir)
        detected = snap.detected_game or "не обнаружена"
        active = ", ".join(snap.active_items) if snap.active_items else "ничего"
        await callback.message.answer(
            "<b>🎮 Игры</b>\n\n"
            f"🕹 <b>Текущая игра:</b> {escape(detected)}\n"
            f"🧩 <b>Активно:</b> {escape(active)}"
        )

    elif action == "files":
        items = list_allowed_files(config.data_dir)
        if not items:
            await callback.message.answer("<b>📁 Файлы</b>\n\nСписок пуст.")
        else:
            text = "<b>📁 Файлы</b>\n\n" + "\n".join(
                f"• {escape(item)}" for item in items[:20]
            )
            await callback.message.answer(text)

    elif action == "media":
        await callback.message.answer(
            "<b>🎵 Медиа</b>\n\nВыбери действие.",
            reply_markup=media_keyboard(),
        )

    elif action == "power":
        await callback.message.answer(
            "<b>⚡ Питание</b>\n\nИспользуй /power для подтверждения действия."
        )

    elif action == "help":
        await callback.message.answer(
            "<b>ℹ️ Помощь</b>\n\n"
            "Это бот для быстрого управления ПК.\n"
            "Основное: система, игры, сценарии и запуск приложений."
        )

    await callback.answer()


@router.callback_query(F.data.startswith("system:"))
async def system_action_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    action = callback.data.split(":", 1)[1]

    if action == "status":
        snap = get_system_snapshot()
        text = (
            "<b>🖥 Статус</b>\n\n"
            f"🔥 <b>CPU:</b> {snap['cpu_percent']:.1f}%\n"
            f"🧠 <b>RAM:</b> {snap['memory_percent']:.1f}%\n"
            f"💿 <b>Disk:</b> {snap['disk_percent']:.1f}%"
        )
        await callback.message.answer(text)

    elif action == "processes":
        rows = top_processes()
        if not rows:
            await callback.message.answer("<b>📊 Процессы</b>\n\nСписок пуст.")
        else:
            text = "<b>📊 Процессы</b>\n\n" + "\n".join(
                f"• <b>{escape(str(row['name']))}</b> — "
                f"CPU {row['cpu_percent']:.1f}% | RAM {row['memory_mb']:.1f} MB"
                for row in rows
            )
            await callback.message.answer(text)

    elif action == "ping":
        ok, message = ping_host("8.8.8.8")
        prefix = "✅" if ok else "❌"
        await callback.message.answer(f"<b>🌐 Ping</b>\n\n{prefix} {escape(message)}")

    await callback.answer()


@router.callback_query(F.data.startswith("media:"))
async def media_action_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    parts = callback.data.split(":")

    if len(parts) == 2 and parts[1] == "mute":
        ok, message = mute_volume()
        prefix = "✅" if ok else "❌"
        await callback.message.answer(f"<b>🎵 Медиа</b>\n\n{prefix} {escape(message)}")
        await callback.answer()
        return

    if len(parts) == 3 and parts[1] == "vol":
        level = int(parts[2])
        ok, message = set_volume(level)
        prefix = "✅" if ok else "❌"
        await callback.message.answer(f"<b>🎵 Медиа</b>\n\n{prefix} {escape(message)}")
        await callback.answer()
        return

    await callback.answer("Неизвестное действие.", show_alert=False)


@router.callback_query(F.data.startswith("app:"))
async def app_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    app_key = callback.data.split(":", 1)[1]
    ok, result = open_allowed_app(config.data_dir, app_key)
    prefix = "✅" if ok else "❌"
    await callback.message.answer(f"<b>📦 Приложения</b>\n\n{prefix} {escape(result)}")
    await callback.answer()


@router.callback_query(F.data.startswith("scenario:"))
async def scenario_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    scenario_key = callback.data.split(":", 1)[1]
    lines = run_scenario(config.data_dir, scenario_key)
    await callback.message.answer("\n".join(lines))
    await callback.answer()


@router.callback_query(F.data.startswith("confirm:"))
async def confirm_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    key = callback.data.split(":", 1)[1]
    item = store.get(key)

    if not item:
        await callback.answer("Подтверждение истекло.", show_alert=True)
        return

    store.delete(key)

    if item.action == "shutdown":
        ok, message = shutdown_pc()
        prefix = "✅" if ok else "❌"
        await callback.message.answer(f"{prefix} {escape(message)}")
        await callback.answer()
        return

    await callback.answer("Неизвестное действие.", show_alert=True)


@router.callback_query(F.data.startswith("cancel:"))
async def cancel_callback(callback: CallbackQuery, config: AppConfig) -> None:
    if not await ensure_authorized(callback, config):
        return

    key = callback.data.split(":", 1)[1]
    store.delete(key)

    await callback.answer("Отменено.")
    await callback.message.answer("<b>❌ Действие отменено.</b>")