# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import os
import sys

from . import PROJECT, Root


def time_formatter(
    ms: int | float,
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
        os.system("clear")
    try:
        import psutil

        proc = psutil.Process(os.getpid())
        for p in proc.open_files() + proc.connections():
            os.close(p.fd)
    except BaseException:
        pass
    if update:
        reqs = Root / "requirements.txt"
        os.system(f"{sys.executable} -m pip install --disable-pip-version-check --default-timeout=100 -U -r {reqs}")
    os.execl(sys.executable, sys.executable, "-m", PROJECT)
