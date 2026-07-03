from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from services.apps_service import open_allowed_app
from services.system_service import (
    get_health_status,
    get_heavy_processes,
    mute_volume,
    ping_host,
    set_volume,
)
from utils.yaml_loader import load_yaml


@dataclass(slots=True)
class Scenario:
    key: str
    description: str
    require_confirmation: bool
    steps: list[dict[str, Any]]


def load_scenarios(data_dir: Path) -> dict[str, Scenario]:
    data = load_yaml(data_dir / "scenarios.yaml")
    result: dict[str, Scenario] = {}

    for key, value in data.get("scenarios", {}).items():
        result[key] = Scenario(
            key=key,
            description=value.get("description", ""),
            require_confirmation=bool(value.get("require_confirmation", False)),
            steps=value.get("steps", []),
        )

    return result


def run_scenario(data_dir: Path, scenario_key: str) -> list[str]:
    scenarios = load_scenarios(data_dir)
    scenario = scenarios.get(scenario_key)

    if not scenario:
        return ["❌ Сценарий не найден."]

    title = scenario.description.strip() or scenario.key
    results: list[str] = [f"🚀 <b>{title}</b>"]

    for index, step in enumerate(scenario.steps, start=1):
        step_type = step.get("type")

        try:
            if step_type == "open_app":
                app_key = step.get("app", "")
                ok, message = open_allowed_app(data_dir, app_key)
                prefix = "✅" if ok else "❌"
                results.append(f"{index}. {prefix} {message}")

            elif step_type == "health_check":
                health = get_health_status()
                results.append(
                    f"{index}. ✅ CPU: {health.cpu_percent:.1f}% | "
                    f"RAM: {health.memory_percent:.1f}% | "
                    f"Disk: {health.disk_percent:.1f}%"
                )

            elif step_type == "ping_check":
                host = step.get("host", "8.8.8.8")
                ok, message = ping_host(host)
                prefix = "✅" if ok else "❌"
                results.append(f"{index}. {prefix} {message}")

            elif step_type == "show_heavy_apps":
                heavy = get_heavy_processes(limit=5)
                if not heavy:
                    results.append(f"{index}. ⚠️ Ничего тяжёлого не найдено.")
                else:
                    lines = [
                        f"• {proc.name} (PID {proc.pid}) — CPU {proc.cpu_percent:.1f}% | RAM {proc.memory_mb:.1f} MB"
                        for proc in heavy
                    ]
                    results.append(f"{index}. ✅ Топ приложений:\n" + "\n".join(lines))

            elif step_type == "set_volume":
                level = int(step.get("level", 50))
                ok, message = set_volume(level)
                prefix = "✅" if ok else "❌"
                results.append(f"{index}. {prefix} {message}")

            elif step_type == "mute_volume":
                ok, message = mute_volume()
                prefix = "✅" if ok else "❌"
                results.append(f"{index}. {prefix} {message}")

            else:
                results.append(f"{index}. ❌ Неизвестное действие.")

        except Exception as exc:
            results.append(f"{index}. ❌ Не удалось выполнить шаг: {exc}")

    return results