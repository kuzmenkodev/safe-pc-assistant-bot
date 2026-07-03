from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="🚀 Запуск бота"),
        BotCommand(command="help", description="📖 Список команд"),
        BotCommand(command="open", description="📦 Открыть приложение"),
        BotCommand(command="runningapps", description="🖥 Запущенные приложения"),
        BotCommand(command="gaming", description="🎮 Игровой статус"),
        BotCommand(command="cs2", description="🎯 Запустить CS2"),
        BotCommand(command="shutdown", description="⏻ Выключить ПК"),
        BotCommand(command="restart", description="🔄 Перезагрузить ПК"),
    ]
    await bot.set_my_commands(commands)