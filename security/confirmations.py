from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(slots=True)
class PendingConfirmation:
    user_id: int
    action: str
    payload: str
    expires_at: float


class ConfirmationStore:
    def __init__(self, ttl_seconds: int) -> None:
        self.ttl_seconds = ttl_seconds
        self._items: dict[str, PendingConfirmation] = {}

    def create(self, key: str, user_id: int, action: str, payload: str) -> None:
        self._items[key] = PendingConfirmation(user_id=user_id, action=action, payload=payload, expires_at=time.time() + self.ttl_seconds)

    def get(self, key: str) -> PendingConfirmation | None:
        item = self._items.get(key)
        if not item:
            return None
        if item.expires_at < time.time():
            self._items.pop(key, None)
            return None
        return item

    def delete(self, key: str) -> None:
        self._items.pop(key, None)
