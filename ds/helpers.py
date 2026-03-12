# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import os
import shutil
import subprocess
import sys

from . import PROJECT, Root


def time_formatter(
    dur: float,
    readable: bool = False,
) -> str:
    if dur > 1e10:
        dur //= 1000
    total = int(dur)
    sec = total % 60
    total //= 60
    mins = total % 60
    total //= 60
    hour = total % 24
    total //= 24
    day = total % 7
    week = total // 7
    if not (week or day or hour or mins or sec):
        return "0sec" if readable else "0s"
    if readable:
        parts = []
        if week:
            parts.append(f"{week}week")
        if day:
            parts.append(f"{day}day")
        if hour:
            parts.append(f"{hour}hour")
        if mins:
            parts.append(f"{mins}min")
        if sec:
            parts.append(f"{sec}sec")
        return ", ".join(parts)
    parts = []
    if week:
        parts.append(f"{week}w")
    if day:
        parts.append(f"{day}d")
    if hour:
        parts.append(f"{hour}h")
    if mins:
        parts.append(f"{mins}m")
    if sec:
        parts.append(f"{sec}s")
    return ", ".join(parts)


def get_terminal_logs() -> list[str]:
    return sorted(map(str, (Root / "logs").rglob("*.log")))


def restart(update: bool = False) -> None:
    if update:
        reqs = str(Root / "requirements.txt")
        if shutil.which("uv"):
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
        else:
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
