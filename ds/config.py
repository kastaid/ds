# ruff: noqa: RUF012
# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

from os import getenv

from dotenv import load_dotenv

from . import WORKERS, Root

load_dotenv(Root / ".env", override=True)


def env(key: str, default: str = "") -> str:
    return getenv(key, default).strip()


def to_bool(value: str) -> bool:
    value = value.lower()
    if value in {"y", "yes", "t", "true", "on", "1", "enable", "enabled"}:
        return True
    if value in {"n", "no", "f", "false", "off", "0", "disable", "disabled"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


class Var:
    DEV_MODE: bool = to_bool(env("DEV_MODE", "false"))
    API_ID: int = int(env("API_ID", "0"))
    API_HASH: str = env("API_HASH", "")
    STRING_SESSION: str = env("STRING_SESSION", "")
    HANDLER: str = env("HANDLER", "")
    WORKERS: int = int(env("WORKERS", str(WORKERS)))
    IS_STARTUP: bool = False
    ERROR_RETRY: dict[int, int] = {}


del load_dotenv, WORKERS, Root
