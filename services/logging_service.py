from __future__ import annotations

import logging
from pathlib import Path


def setup_logging(log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "bot.log"
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.handlers:
        root_logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)