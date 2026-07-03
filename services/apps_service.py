from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import psutil

from utils.yaml_loader import load_yaml


@dataclass(slots=True)
class AppEntry:
    key: str
    display_name: str
    path: str
    args: list[str]
    process_names: list[str]
    allow_close: bool


def load_apps(data_dir: Path) -> dict[str, AppEntry]:
    data = load_yaml(data_dir / 'apps.yaml')
    result: dict[str, AppEntry] = {}
    for key, value in data.get('apps', {}).items():
        result[key] = AppEntry(
            key=key,
            display_name=value.get('display_name', key),
            path=value.get('path', ''),
            args=value.get('args', []),
            process_names=value.get('process_names', []),
            allow_close=bool(value.get('allow_close', False)),
        )
    return result


def open_allowed_app(data_dir: Path, app_key: str) -> tuple[bool, str]:
    apps = load_apps(data_dir)
    app = apps.get(app_key)
    if not app:
        return False, 'App not found in allowlist.'
    if not Path(app.path).exists():
        return False, f'Path does not exist: {app.path}'
    subprocess.Popen([app.path, *app.args], shell=False)
    return True, f'Started: {app.display_name}'


def running_allowlisted_apps(data_dir: Path) -> list[str]:
    apps = load_apps(data_dir)
    names: dict[str, str] = {}
    for app in apps.values():
        for proc in app.process_names:
            names[proc.lower()] = app.display_name
    found: set[str] = set()
    for proc in psutil.process_iter(['name']):
        try:
            process_name = (proc.info.get('name') or '').lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if process_name in names:
            found.add(names[process_name])
    return sorted(found)
