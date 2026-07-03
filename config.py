from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _parse_int_list(value: str) -> list[int]:
    if not value:
        return []

    result: list[int] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        result.append(int(part))

    return result


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_int_env(name: str, default: str) -> int:
    raw = os.getenv(name, default).strip()
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got: {raw!r}") from exc


@dataclass(slots=True)
class AppConfig:
    bot_token: str
    bot_name: str = "ПК-ассистент"
    authorized_user_ids: list[int] = field(default_factory=list)
    authorized_chat_ids: list[int] = field(default_factory=list)
    data_dir: Path = field(default_factory=lambda: Path("./data").resolve())
    log_dir: Path = field(default_factory=lambda: Path("./logs").resolve())
    alerts_enabled: bool = True
    default_parse_mode: str = "HTML"
    rate_limit_commands_per_minute: int = 20
    confirmation_ttl_seconds: int = 30
    download_timeout_seconds: int = 60
    max_download_size_mb: int = 100

    @classmethod
    def from_env(cls) -> "AppConfig":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError("BOT_TOKEN is missing in environment")

        config = cls(
            bot_token=token,
            bot_name=os.getenv("BOT_NAME", "ПК-ассистент").strip() or "ПК-ассистент",
            authorized_user_ids=_parse_int_list(os.getenv("AUTHORIZED_USER_IDS", "")),
            authorized_chat_ids=_parse_int_list(os.getenv("AUTHORIZED_CHAT_IDS", "")),
            data_dir=Path(os.getenv("DATA_DIR", "./data")).resolve(),
            log_dir=Path(os.getenv("LOG_DIR", "./logs")).resolve(),
            alerts_enabled=_parse_bool(os.getenv("ALERTS_ENABLED"), True),
            default_parse_mode=os.getenv("DEFAULT_PARSE_MODE", "HTML").strip() or "HTML",
            rate_limit_commands_per_minute=_parse_int_env("RATE_LIMIT_COMMANDS_PER_MINUTE", "20"),
            confirmation_ttl_seconds=_parse_int_env("CONFIRMATION_TTL_SECONDS", "30"),
            download_timeout_seconds=_parse_int_env("DOWNLOAD_TIMEOUT_SECONDS", "60"),
            max_download_size_mb=_parse_int_env("MAX_DOWNLOAD_SIZE_MB", "100"),
        )

        if not config.authorized_user_ids and not config.authorized_chat_ids:
            raise RuntimeError(
                "Set AUTHORIZED_USER_IDS or AUTHORIZED_CHAT_IDS in environment"
            )

        config.data_dir.mkdir(parents=True, exist_ok=True)
        config.log_dir.mkdir(parents=True, exist_ok=True)

        return config