from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import psutil

from utils.yaml_loader import load_yaml


@dataclass(slots=True)
class GamingSnapshot:
    active_items: list[str]
    detected_game: str | None


def load_game_map(data_dir: Path) -> tuple[dict[str, str], dict[str, str]]:
    data = load_yaml(data_dir / 'games.yaml')
    game_map: dict[str, str] = {}
    launcher_map: dict[str, str] = {}
    for item in data.get('games', {}).values():
        display_name = item.get('display_name', 'Unknown Game')
        for proc_name in item.get('process_names', []):
            game_map[proc_name.lower()] = display_name
    for item in data.get('launchers', {}).values():
        display_name = item.get('display_name', 'Unknown Launcher')
        for proc_name in item.get('process_names', []):
            launcher_map[proc_name.lower()] = display_name
    return game_map, launcher_map


def get_gaming_snapshot(data_dir: Path) -> GamingSnapshot:
    game_map, launcher_map = load_game_map(data_dir)
    active: list[str] = []
    detected_game: str | None = None
    for proc in psutil.process_iter(['name']):
        try:
            name = (proc.info.get('name') or '').lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if name in game_map:
            active.append(game_map[name])
            if detected_game is None:
                detected_game = game_map[name]
        if name in launcher_map:
            active.append(launcher_map[name])
    return GamingSnapshot(active_items=sorted(set(active)), detected_game=detected_game)
