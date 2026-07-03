from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from utils.yaml_loader import load_yaml


@dataclass(slots=True)
class Scenario:
    key: str
    description: str
    require_confirmation: bool
    steps: list[dict[str, Any]]


def load_scenarios(data_dir: Path) -> dict[str, Scenario]:
    data = load_yaml(data_dir / 'scenarios.yaml')
    result: dict[str, Scenario] = {}
    for key, value in data.get('scenarios', {}).items():
        result[key] = Scenario(
            key=key,
            description=value.get('description', ''),
            require_confirmation=bool(value.get('require_confirmation', False)),
            steps=value.get('steps', []),
        )
    return result
