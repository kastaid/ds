# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import os
import platform
import subprocess
import sys
from asyncio import sleep
from sqlite3 import OperationalError
from time import time
from typing import Any
from pyrogram.client import Client as RawClient
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors import FloodWait, NotAcceptable, Unauthorized
from pyrogram.types import User
from . import (
    __version__,
    PROJECT,
    StartTime,
    Root,
)
from .config import Var
from .helpers import time_formatter, restart
from .logger import LOGS


class Client(RawClient):
    def __init__(self, **kwargs: Any):
        self._me: User | None = None
        self._is_bot: bool = bool(kwargs.get("bot_token", None))
        self.logs = LOGS
        super().__init__(**kwargs)

    @property
    def is_bot(self) -> bool:
        return self._is_bot

    async def get_me(self, cached: bool = True) -> User:
        if not cached or self._me is None:
            self._me = await super().get_me()
        return self._me

    async def start(self):
        try:
            self.logs.info("Starting {} Client...".format(self.is_bot and "Bot" or "User"))
            await super().start()
        except FloodWait as fw:
            self.logs.warning(fw)
            await sleep(fw.value)
            await super().start()
        except OperationalError as err:
            if str(err) == "database is locked" and os.name == "posix":
                self.logs.warning("Session file is locked. Trying to kill blocking process...")
                subprocess.run(["fuser", "-k", f"{PROJECT}.session"])
                restart()
            raise
        except (NotAcceptable, Unauthorized) as err:
            self.logs.error(f"{err.__class__.__name__}: {err}\nMoving session file to {PROJECT}.session-old...")
            os.rename(f"./{PROJECT}.session", f"./{PROJECT}.session-old")
            restart()
        except Exception as err:
            self.logs.exception(err)
            self.logs.error("Client start exiting.")
            sys.exit(1)
        self.me = await self.get_me()
        self.logs.info(
            f"Client details:\nID: {self.me.id}\nFirst Name: {self.me.first_name}\nLast Name: {self.me.last_name}\nUsername: {self.me.username}"
        )
        done = time_formatter((time() - StartTime) * 1000)
        self.logs.success(f">> 🔥 USERBOT IS RUNNING IN {done} !!")

    async def stop(self, *args):
        try:
            await super().stop()
        except BaseException:
            pass


User = Client(
    name=PROJECT,
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    app_version=__version__,
    device_model=PROJECT + "v" + __version__,
    session_string=Var.STRING_SESSION,
    workers=Var.WORKERS,
    workdir=Root,
    parse_mode=ParseMode.HTML,
    system_version=platform.version() + " " + platform.machine(),
    sleep_threshold=30,
    plugins={
        "root": PROJECT + ".plugins",
        "exclude": [],
    },
)
