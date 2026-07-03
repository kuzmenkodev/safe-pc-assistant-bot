from __future__ import annotations

from pathlib import Path

from security.path_guard import is_safe_child
from utils.yaml_loader import load_yaml


def load_allowed_roots(data_dir: Path) -> list[Path]:
    data = load_yaml(data_dir / 'folders.yaml')
    return [Path(item) for item in data.get('folders', {}).get('allowed_roots', [])]


def list_allowed_files(data_dir: Path) -> list[str]:
    roots = load_allowed_roots(data_dir)
    results: list[str] = []
    for root in roots:
        if not root.exists():
            continue
        for item in root.iterdir():
            if item.is_file() and is_safe_child(item, roots):
                results.append(str(item))
    return sorted(results)[:30]
