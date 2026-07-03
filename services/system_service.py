from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass

import psutil
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


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


def _get_volume_controller():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def get_health_status() -> HealthStatus:
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:\\").percent
    return HealthStatus(
        cpu_percent=cpu,
        memory_percent=memory,
        disk_percent=disk,
    )


def get_system_snapshot() -> dict[str, float]:
    health = get_health_status()
    return {
        "cpu_percent": health.cpu_percent,
        "memory_percent": health.memory_percent,
        "disk_percent": health.disk_percent,
    }


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


def set_volume(level: int) -> tuple[bool, str]:
    try:
        level = max(0, min(100, int(level)))
        volume = _get_volume_controller()
        volume.SetMute(0, None)
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return True, f"Volume set to {level}%."
    except Exception as exc:
        return False, f"Volume error: {exc}"


def mute_volume() -> tuple[bool, str]:
    try:
        volume = _get_volume_controller()
        volume.SetMute(1, None)
        return True, "Volume muted."
    except Exception as exc:
        return False, f"Mute error: {exc}"


def top_processes(limit: int = 5) -> list[dict[str, float | int | str]]:
    items = get_heavy_processes(limit=limit)
    return [
        {
            "pid": item.pid,
            "name": item.name,
            "cpu_percent": item.cpu_percent,
            "memory_mb": item.memory_mb,
        }
        for item in items
    ]