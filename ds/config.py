# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

from asyncio import Event
from os import getenv

from dotenv import load_dotenv

from . import Root

load_dotenv(Root / ".env", override=True)


def to_bool(value: str) -> bool:
    value = value.lower()
    if value in {"y", "yes", "t", "true", "on", "1", "enable", "enabled"}:
        return True
    if value in {"n", "no", "f", "false", "off", "0", "disable", "disabled"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def env(key: str, default: str = "") -> str:
    return getenv(key, default).strip()


class Var:
    DEV_MODE: bool = to_bool(env("DEV_MODE", "false"))
    WORKERS: int = int(env("WORKERS", "3"))
    API_ID: int = int(env("API_ID", "0"))
    API_HASH: str = env("API_HASH", "")
    STRING_SESSION: str = env("STRING_SESSION", "")
    HANDLER: str = env("HANDLER", "")
    IS_STARTUP: bool = False
    STARTUP_EVENT: Event = Event()
