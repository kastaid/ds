# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from os import getenv
from typing import ClassVar
from dotenv import load_dotenv, find_dotenv
from . import WORKERS

load_dotenv(find_dotenv("config.env"))


def tobool(val: str) -> int | None:
    """
    Convert a string representation of truth to true (1) or false (0).
    https://github.com/python/cpython/blob/main/Lib/distutils/util.py
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    if val in ("n", "no", "f", "false", "off", "0"):
        return 0
    raise ValueError("invalid truth value %r" % (val,))


class Var:
    DEV_MODE: bool = tobool(getenv("DEV_MODE", "false").strip())
    API_ID: int = int(getenv("API_ID", "0").strip())
    API_HASH: str = getenv("API_HASH", "").strip()
    STRING_SESSION: str = getenv("STRING_SESSION", "").strip()
    WORKERS: int = int(getenv("WORKERS", str(WORKERS)).strip())
    HANDLER: str = getenv("HANDLER", "").strip()
    IS_STARTUP: bool = False
    DS_TASKS: ClassVar[dict[int, set[int]]] = {i: set() for i in range(10)}
    ERROR_RETRY: ClassVar[dict[int, int]] = {}


del load_dotenv, find_dotenv, WORKERS
