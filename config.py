from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _parse_int_list(value: str) -> List[int]:
    if not value:
        return []
    return [int(part.strip()) for part in value.split(",") if part.strip()]


def _parse_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class AppConfig:
    bot_token: str
    bot_name: str = "ПК-ассистент"
    authorized_user_ids: List[int] = field(default_factory=list)
    authorized_chat_ids: List[int] = field(default_factory=list)
    data_dir: Path = Path("./data")
    log_dir: Path = Path("./logs")
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

        return cls(
            bot_token=token,
            bot_name=os.getenv("BOT_NAME", "ПК-ассистент"),
            authorized_user_ids=_parse_int_list(os.getenv("AUTHORIZED_USER_IDS", "")),
            authorized_chat_ids=_parse_int_list(os.getenv("AUTHORIZED_CHAT_IDS", "")),
            data_dir=Path(os.getenv("DATA_DIR", "./data")),
            log_dir=Path(os.getenv("LOG_DIR", "./logs")),
            alerts_enabled=_parse_bool(os.getenv("ALERTS_ENABLED"), True),
            default_parse_mode=os.getenv("DEFAULT_PARSE_MODE", "HTML"),
            rate_limit_commands_per_minute=int(os.getenv("RATE_LIMIT_COMMANDS_PER_MINUTE", "20")),
            confirmation_ttl_seconds=int(os.getenv("CONFIRMATION_TTL_SECONDS", "30")),
            download_timeout_seconds=int(os.getenv("DOWNLOAD_TIMEOUT_SECONDS", "60")),
            max_download_size_mb=int(os.getenv("MAX_DOWNLOAD_SIZE_MB", "100")),
        )