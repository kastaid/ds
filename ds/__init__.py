# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import set_event_loop
from multiprocessing import cpu_count
from pathlib import Path
from shutil import rmtree
from time import time
import uvloop
from version import __version__

PROJECT = "ds"
StartTime = time()
Root: Path = Path(__file__).parent.parent
LOOP = uvloop.new_event_loop()
set_event_loop(LOOP)
WORKERS = cpu_count() * 5

DIRS = ("logs/",)
for d in DIRS:
    if not (Root / d).exists():
        (Root / d).mkdir(parents=True, exist_ok=True)
    else:
        for _ in (Root / d).rglob("*"):
            if _.is_dir():
                rmtree(_)
            else:
                _.unlink(missing_ok=True)

del set_event_loop, uvloop, Path, cpu_count, rmtree, time
