# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import sys
from asyncio import sleep
from contextlib import suppress
from platform import version, machine
from random import randrange
from time import time
from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import RPCError
from pyrogram.types import User, CallbackQuery
from . import PROJECT, StartTime, Root
from .config import Var
from .helpers import time_formatter


class UserClient(Client):
    def __init__(self):
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
            plugins={
                "root": "".join((PROJECT, ".plugins")),
                "exclude": [],
            },
            sleep_threshold=15,
        )

    async def get_me(
        self,
        cached: bool = True,
    ) -> User:
        if not cached or self._me is None:
            self._me = await super().get_me()
        return self._me

    async def start(self) -> None:
        try:
            self.log.info("Starting Userbot Client...")
            await sleep(randrange(3, 6))
            await super().start()
        except Exception as err:
            self.log.exception(err)
            self.log.error("Userbot Client exiting.")
            sys.exit(1)
        self.me = await self.get_me()
        user_details = f"Userbot Client details:\nID: {self.me.id}\nFirst Name: {self.me.first_name}"
        user_details += f"\nLast Name: {self.me.last_name}" if self.me.last_name else ""
        user_details += f"\nUsername: {self.me.username}" if self.me.username else ""
        self.log.info(user_details)
        await self.join_us()
        done = time_formatter((time() - StartTime) * 1000)
        self.log.success(f">> 🔥 USERBOT RUNNING IN {done} !!")
        Var.IS_STARTUP = True

    async def join_us(self) -> None:
        with suppress(BaseException):
            await self.join_chat(-1001174631272)
            await sleep(3)
        with suppress(BaseException):
            await self.join_chat(-1001699144606)

    async def answer(
        self,
        callback: CallbackQuery,
        **args,
    ) -> None:
        try:
            await callback.answer(**args)
        except RPCError:
            pass

    async def try_delete(self, event) -> bool:
        if not event:
            return False
        is_callback = isinstance(event, CallbackQuery)
        message = event.message if is_callback else event
        deleted = await message.delete()
        if not deleted and is_callback:
            await self.answer(event)
        return deleted

    async def stop(self, **_) -> None:
        try:
            await super().stop()
            self.log.info("Stopped Client.")
        except BaseException:
            pass
