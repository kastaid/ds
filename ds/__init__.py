# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from os import cpu_count
from pathlib import Path
from shutil import rmtree
from time import time

from version import __version__  # noqa

PROJECT = "ds"
StartTime = time()
Root: Path = Path(__file__).parent.parent
WORKERS = min(32, (cpu_count() or 1) + 4)

for d in ("logs/",):
    if not (Root / d).exists():
        (Root / d).mkdir(parents=True, exist_ok=True)
    else:
        for _ in (Root / d).rglob("*"):
            if _.is_dir():
                rmtree(_, ignore_errors=True)
            else:
                _.unlink(missing_ok=True)

del cpu_count, Path, rmtree, time
