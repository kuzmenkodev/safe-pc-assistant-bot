from __future__ import annotations

from pathlib import Path

from security.path_guard import is_safe_child
from utils.yaml_loader import load_yaml


def load_files_config(data_dir: Path) -> dict:
    return load_yaml(data_dir / "folders.yaml")


def load_allowed_roots(data_dir: Path) -> list[Path]:
    data = load_files_config(data_dir)
    return [Path(item) for item in data.get("folders", {}).get("allowed_roots", [])]


def load_allowed_extensions(data_dir: Path) -> set[str]:
    data = load_files_config(data_dir)
    return {ext.lower() for ext in data.get("limits", {}).get("allowed_extensions", [])}


def load_max_file_size_mb(data_dir: Path) -> int | None:
    data = load_files_config(data_dir)
    value = data.get("limits", {}).get("max_file_size_mb")
    return int(value) if value is not None else None


def list_allowed_files(data_dir: Path) -> list[str]:
    roots = load_allowed_roots(data_dir)
    allowed_extensions = load_allowed_extensions(data_dir)
    max_file_size_mb = load_max_file_size_mb(data_dir)

    results: list[str] = []

    for root in roots:
        if not root.exists() or not root.is_dir():
            continue

        for item in root.iterdir():
            if not item.is_file():
                continue

            if not is_safe_child(item, roots):
                continue

            if allowed_extensions and item.suffix.lower() not in allowed_extensions:
                continue

            if max_file_size_mb is not None:
                size_mb = item.stat().st_size / 1024 / 1024
                if size_mb > max_file_size_mb:
                    continue

            results.append(str(item))

    return sorted(results)[:30]