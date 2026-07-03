from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def apps_keyboard(apps: dict) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"📦 {app.display_name}", callback_data=f"app:{key}")]
        for key, app in apps.items()
    ]
    rows.append(
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:main"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def scenarios_keyboard(scenarios: dict) -> InlineKeyboardMarkup:
    rows = []

    for key, scenario in scenarios.items():
        title = getattr(scenario, "description", "") or key
        rows.append(
            [InlineKeyboardButton(text=f"🚀 {title}", callback_data=f"scenario:{key}")]
        )

    rows.append(
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:main"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def system_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖥 Статус", callback_data="system:status"),
                InlineKeyboardButton(text="📊 Процессы", callback_data="system:processes"),
            ],
            [
                InlineKeyboardButton(text="🌐 Ping", callback_data="system:ping"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:main"),
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"),
            ],
        ]
    )


def media_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔈 25%", callback_data="media:vol:25"),
                InlineKeyboardButton(text="🔉 50%", callback_data="media:vol:50"),
                InlineKeyboardButton(text="🔊 75%", callback_data="media:vol:75"),
            ],
            [
                InlineKeyboardButton(text="💯 100%", callback_data="media:vol:100"),
                InlineKeyboardButton(text="🔇 Без звука", callback_data="media:mute"),
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:main"),
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu:main"),
            ],
        ]
    )