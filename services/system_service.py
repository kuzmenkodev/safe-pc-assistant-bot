from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass

import psutil


@dataclass(slots=True)
class HealthStatus:
    cpu_percent: float
    memory_percent: float
    disk_percent: float


@dataclass(slots=True)
class ProcessEntry:
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float


def get_health_status() -> HealthStatus:
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:\\").percent
    return HealthStatus(
        cpu_percent=cpu,
        memory_percent=memory,
        disk_percent=disk,
    )


def get_heavy_processes(limit: int = 5) -> list[ProcessEntry]:
    processes = list(psutil.process_iter(["pid", "name"]))
    for proc in processes:
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(0.3)

    result: list[ProcessEntry] = []
    for proc in processes:
        try:
            cpu = proc.cpu_percent(interval=None)
            memory_mb = proc.memory_info().rss / 1024 / 1024
            result.append(
                ProcessEntry(
                    pid=proc.pid,
                    name=proc.info.get("name") or "unknown",
                    cpu_percent=cpu,
                    memory_mb=memory_mb,
                )
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    result.sort(key=lambda x: (x.cpu_percent, x.memory_mb), reverse=True)
    return result[:limit]


def ping_host(host: str = "8.8.8.8") -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            ["ping", "-n", "1", host],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
        )
        if completed.returncode == 0:
            return True, f"Ping OK: {host}"
        return False, f"Ping failed: {host}"
    except Exception as exc:
        return False, f"Ping error: {exc}"