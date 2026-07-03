from __future__ import annotations


def format_hours(hours: float) -> str:
    if hours < 1:
        return f'{int(hours * 60)} min'
    return f'{hours:.1f} h'
