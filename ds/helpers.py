# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import os
import subprocess
import sys

from . import (
    LOG_DIR,
    PROJECT,
    Root,
)


def format_time(
    elapsed: float,
    readable: bool = False,
    short: bool = False,
) -> str:
    total = int(elapsed)
    ms = int((elapsed - total) * 1000)
    sec = total % 60
    total //= 60
    mins = total % 60
    total //= 60
    hour = total % 24
    total //= 24
    day = total % 30
    total //= 30
    month = total % 12
    year = total // 12
    week = day // 7
    day %= 7
    if short:
        if year:
            day = hour = mins = sec = ms = 0
        elif week:
            mins = sec = ms = 0
        elif day:
            sec = ms = 0
        elif hour or sec:
            ms = 0
    if not (year or month or week or day or hour or mins or sec or ms):
        return "0 seconds" if readable else "0s"
    p = []
    if readable:
        if year:
            p.append(f"{year} year{'s' if year > 1 else ''}")
        if month:
            p.append(f"{month} month{'s' if month > 1 else ''}")
        if week:
            p.append(f"{week} week{'s' if week > 1 else ''}")
        if day:
            p.append(f"{day} day{'s' if day > 1 else ''}")
        if hour:
            p.append(f"{hour} hour{'s' if hour > 1 else ''}")
        if mins:
            p.append(f"{mins} minute{'s' if mins > 1 else ''}")
        if sec:
            p.append(f"{sec} second{'s' if sec > 1 else ''}")
        if ms:
            p.append(f"{ms} millisecond{'s' if ms > 1 else ''}")
    else:
        if year:
            p.append(f"{year}y")
        if month:
            p.append(f"{month}mo")
        if week:
            p.append(f"{week}w")
        if day:
            p.append(f"{day}d")
        if hour:
            p.append(f"{hour}h")
        if mins:
            p.append(f"{mins}m")
        if sec:
            p.append(f"{sec}s")
        if ms:
            p.append(f"{ms}ms")
    return ", ".join(p)


def format_latency(elapsed: float) -> str:
    return f"{elapsed * 1000:.0f}ms" if elapsed < 0.1 else f"{elapsed:.2f}s"


def get_terminal_logs() -> list[str]:
    return sorted(map(str, LOG_DIR.glob("*.log")))


def restart(update: bool = False) -> None:
    if update:
        reqs = str(Root / "requirements.txt")
        try:
            subprocess.run(
                [
                    "uv",
                    "pip",
                    "install",
                    "-r",
                    reqs,
                ],
                check=True,
            )
        except FileNotFoundError:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--prefer-binary",
                    "--disable-pip-version-check",
                    "--default-timeout=100",
                    "-r",
                    reqs,
                ],
                check=True,
            )
    os.execl(sys.executable, sys.executable, "-m", PROJECT)
