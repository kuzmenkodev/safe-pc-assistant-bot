from __future__ import annotations

import platform
import shutil
import socket
import time
from dataclasses import dataclass

import psutil


@dataclass(slots=True)
class SystemSnapshot:
    hostname: str
    os_name: str
    uptime_hours: float
    cpu_percent: float
    ram_percent: float
    free_ram_gb: float
    disk_percent: float
    local_ip: str


def get_local_ip() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except OSError:
        return 'unknown'


def get_system_snapshot() -> SystemSnapshot:
    vm = psutil.virtual_memory()
    disk = shutil.disk_usage('/')
    uptime_hours = (time.time() - psutil.boot_time()) / 3600
    return SystemSnapshot(
        hostname=platform.node(),
        os_name=f'{platform.system()} {platform.release()}',
        uptime_hours=round(uptime_hours, 2),
        cpu_percent=psutil.cpu_percent(interval=0.5),
        ram_percent=vm.percent,
        free_ram_gb=round(vm.available / (1024 ** 3), 2),
        disk_percent=round((disk.used / disk.total) * 100, 2),
        local_ip=get_local_ip(),
    )


def top_processes(limit: int = 10) -> list[tuple[str, float, float]]:
    rows: list[tuple[str, float, float]] = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            rows.append((info.get('name') or 'unknown', float(info.get('cpu_percent') or 0.0), float(info.get('memory_percent') or 0.0)))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    rows.sort(key=lambda item: (item[1], item[2]), reverse=True)
    return rows[:limit]
