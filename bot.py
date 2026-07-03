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
from services.logging_service import setup_logging


async def set_main_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Открыть главное меню"),
            BotCommand(command="help", description="Показать команды"),
            BotCommand(command="status", description="Статус ПК"),
            BotCommand(command="processes", description="Топ процессов"),
            BotCommand(command="gaming", description="Игровой статус"),
            BotCommand(command="open", description="Открыть приложение"),
            BotCommand(command="runningapps", description="Запущенные приложения"),
            BotCommand(command="files", description="Разрешённые файлы"),
            BotCommand(command="power", description="Питание"),
            BotCommand(command="scenarios", description="Сценарии"),
            BotCommand(command="autostartinfo", description="Автозапуск Windows"),
        ]
    )


async def main() -> None:
    config = AppConfig.from_env()
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.log_dir.mkdir(parents=True, exist_ok=True)

    setup_logging(config.log_dir)

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML if config.default_parse_mode.upper() == "HTML" else None
        ),
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

    await set_main_commands(bot)

    logging.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())