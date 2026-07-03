from __future__ import annotations

from pathlib import Path


def is_safe_child(path: Path, allowed_roots: list[Path]) -> bool:
    try:
        resolved_path = path.resolve(strict=False)
    except OSError:
        return False

    for root in allowed_roots:
        try:
            resolved_root = root.resolve(strict=False)
        except OSError:
            continue

        try:
            resolved_path.relative_to(resolved_root)
            return True
        except ValueError:
            continue

    return False