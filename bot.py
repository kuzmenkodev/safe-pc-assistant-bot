from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import AppConfig
from handlers.apps import router as apps_router
from handlers.callbacks import router as callbacks_router
from handlers.common import router as common_router
from handlers.files import router as files_router
from handlers.gaming import router as gaming_router
from handlers.media import router as media_router
from handlers.power import router as power_router
from handlers.scenarios import router as scenarios_router
from handlers.system import router as system_router
from keyboards.main import main_menu_keyboard
from services.logging_service import setup_logging


async def send_startup_message(bot: Bot, config: AppConfig) -> None:
    target_chat_id = None

    if config.authorized_chat_ids:
        target_chat_id = config.authorized_chat_ids[0]
    elif config.authorized_user_ids:
        target_chat_id = config.authorized_user_ids[0]

    if target_chat_id is None:
        logging.warning("Startup message skipped: no authorized chat/user id configured")
        return

    text = "<b>✅ Бот онлайн</b>\nГотов к работе."

    try:
        await bot.send_message(
            target_chat_id,
            text,
            reply_markup=main_menu_keyboard(),
        )
    except Exception as exc:
        logging.exception("Failed to send startup message: %s", exc)


async def main() -> None:
    config = AppConfig.from_env()

    setup_logging(config.log_dir)
    logging.info("Starting bot")

    parse_mode = ParseMode.HTML
    if config.default_parse_mode.upper() == "MARKDOWN":
        parse_mode = ParseMode.MARKDOWN_V2

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=parse_mode),
    )
    dp = Dispatcher()

    dp["config"] = config

    dp.include_router(common_router)
    dp.include_router(system_router)
    dp.include_router(gaming_router)
    dp.include_router(apps_router)
    dp.include_router(files_router)
    dp.include_router(media_router)
    dp.include_router(power_router)
    dp.include_router(scenarios_router)
    dp.include_router(callbacks_router)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Открыть главное меню"),
            BotCommand(command="help", description="Информация о боте"),
            BotCommand(command="scenarios", description="Готовые действия"),
            BotCommand(command="power", description="Питание"),
        ]
    )

    if config.alerts_enabled:
        await send_startup_message(bot, config)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()
        logging.info("Bot session closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен вручную.")