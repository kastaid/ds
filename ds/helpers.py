# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import os
import shutil
import subprocess
import sys

from . import PROJECT, Root


def time_formatter(
    ms: float,
    readable: bool = False,
) -> str:
    m, s = divmod(int(ms / 1000), 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    w, d = divmod(d, 7)
    if readable:
        units = [
            (w, "week"),
            (d, "day"),
            (h, "hour"),
            (m, "min"),
            (s, "sec"),
        ]
        parts = [f"{val}{unit}" for val, unit in units if val]
        return ", ".join(parts) or "0sec"
    units = [
        (w, "w"),
        (d, "d"),
        (h, "h"),
        (m, "m"),
        (s, "s"),
    ]
    parts = [f"{val}{unit}" for val, unit in units if val]
    return ", ".join(parts) or "0s"


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
