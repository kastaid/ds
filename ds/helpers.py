# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import os
import sys
from pathlib import Path
from typing import Union
from . import PROJECT, Root


def time_formatter(ms: Union[int, float]) -> str:
    minutes, seconds = divmod(int(ms / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w, ") if weeks else "")
        + ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
    )
    return tmp and tmp[:-2] or "0s"


def get_terminal_logs() -> Path:
    return sorted((Root / "logs").rglob("*.log"))


def restart() -> None:
    os.system("clear")
    try:
        import psutil

        proc = psutil.Process(os.getpid())
        for p in proc.open_files() + proc.connections():
            os.close(p.fd)
    except BaseException:
        pass
    reqs = Root / "requirements.txt"
    os.system(
        f"{sys.executable} -m pip install --disable-pip-version-check --default-timeout=100 --no-cache-dir -U -r {reqs}"
    )
    os.execl(sys.executable, sys.executable, "-m", PROJECT)
