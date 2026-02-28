# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

from pathlib import Path
from shutil import rmtree
from time import time

from version import __version__  # noqa

PROJECT = "ds"
StartTime = time()
Root = Path(__file__).parent.parent
WORKERS = 3

DIRS = ("logs/",)
for d in DIRS:
    if not (Root / d).exists():
        (Root / d).mkdir(parents=True, exist_ok=True)
    else:
        for i in (Root / d).rglob("*"):
            if i.is_dir():
                rmtree(i, ignore_errors=True)
            else:
                i.unlink(missing_ok=True)

del Path, rmtree, time
