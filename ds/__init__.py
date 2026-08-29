# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

from pathlib import Path
from time import monotonic

from version import __version__  # noqa

PROJECT = "ds"

StartTime = monotonic()

Root = Path(__file__).parent.parent
LOG_DIR = Root / "logs"
DATA_DIR = Root / "data"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clean_files(path: Path) -> None:
    if not path.exists():
        return
    for i in path.rglob("*"):
        if i.is_file():
            i.unlink(missing_ok=True)


for path in (
    LOG_DIR,
    DATA_DIR,
):
    ensure_dir(path)
