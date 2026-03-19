# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio
import random
import sys
from platform import machine, version
from time import monotonic
from typing import TYPE_CHECKING

from pyrogram.client import Client as RawClient
from pyrogram.connection.transport import TCPAbridged
from pyrogram.enums import ParseMode
from pyrogram.raw.all import layer

from . import PROJECT, Root, StartTime
from .config import Var
from .helpers import time_formatter
from .logger import LOG

if TYPE_CHECKING:
    from loguru._logger import Logger
    from pyrogram.types import User


class KastaClient(RawClient):
    log: Logger = LOG

    def __init__(self):
        self._stopped: bool = False
        self._me: User | None = None
        super().__init__(
            PROJECT,
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
            session_string=Var.STRING_SESSION,
            workers=Var.WORKERS,
            workdir=Root,
            parse_mode=ParseMode.HTML,
            system_version=" ".join((version(), machine())),
            plugins={"root": "".join((PROJECT, ".plugins")), "exclude": []},
            sleep_threshold=15,
        )
        self.protocol_factory = TCPAbridged

    async def get_me(
        self,
        cached: bool = True,
    ) -> User:
        if not cached or self._me is None:
            self._me = await super().get_me()
        return self._me

    async def start(self) -> KastaClient:
        try:
            if not Var.API_ID:
                raise ValueError("Required: API_ID not set in .env")
            if not Var.API_HASH:
                raise ValueError("Required: API_HASH not set in .env")
            if not Var.STRING_SESSION:
                raise ValueError("Required: STRING_SESSION not set in .env")
            self.log.info(">> 🚀 STARTING USERBOT...")
            _jitter = (3.5, 6.5) if Var.DEV_MODE else (1.5, 3.5)
            await asyncio.sleep(random.uniform(*_jitter))
            await super().start()
            self.me = await self.get_me()
        except Exception as err:
            self.log.exception(err)
            self.log.error(">> USERBOT EXITING.")
            sys.exit(1)
        _me = [
            ">> USERBOT DETAILS:",
            f"ID: {self.me.id}",
            f"First Name: {self.me.first_name}",
        ]
        if self.me.last_name:
            _me.append(f"Last Name: {self.me.last_name}")
        if self.me.username:
            _me.append(f"Username: @{self.me.username}")
        if self.me.dc_id:
            _me.append(f"DC: {self.me.dc_id}")
        _me.append(f"Layer: {layer}")
        self.log.info("\n".join(_me))
        await self.__join_us()
        done = time_formatter(monotonic() - StartTime)
        launch = f">> 🚀 Userbot launched in {done}, layer: {layer}."
        await self.send_message("me", launch)
        self.log.success(f">> 🔥 USERBOT UP IN {done}.")
        Var.IS_STARTUP = True
        return self

    async def stop(self, block: bool = True) -> KastaClient:
        if self._stopped:
            return self
        self._stopped = True
        try:
            await super().stop(block=block)
            self.log.warning(">> USERBOT STOPPED.")
        except BaseException:
            pass
        return self

    async def __join_us(self) -> None:
        try:
            await self.join_chat(-1001174631272)
            await asyncio.sleep(random.uniform(3.5, 6.5))
        except Exception:
            pass
        try:
            await self.join_chat(-1001699144606)
        except Exception:
            pass
