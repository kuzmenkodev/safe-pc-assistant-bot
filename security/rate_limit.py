from __future__ import annotations

import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, limit: int, period_seconds: int = 60) -> None:
        self.limit = limit
        self.period_seconds = period_seconds
        self.storage: dict[int, deque[float]] = defaultdict(deque)

    def hit(self, user_id: int) -> bool:
        now = time.time()
        queue = self.storage[user_id]
        while queue and now - queue[0] > self.period_seconds:
            queue.popleft()
        if len(queue) >= self.limit:
            return False
        queue.append(now)
        return True
