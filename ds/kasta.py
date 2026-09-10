# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio
import random
import signal
import sys
from time import monotonic
from typing import TYPE_CHECKING

from pyrogram import (
    enums,
    errors,
    types,
)
from pyrogram.client import Client as BaseClient
from pyrogram.connection.transport import TCPAbridged
from pyrogram.raw.all import layer
from pyrogram.raw.functions.channels import (
    JoinChannel,
    ReadHistory,
)
from pyrogram.raw.functions.messages import (
    GetHistory,
    GetMessagesViews,
)

from . import (
    DATA_DIR,
    PROJECT,
    StartTime,
)
from .config import Var
from .helpers import format_time
from .logger import LOG

if TYPE_CHECKING:
    from collections.abc import Coroutine

    from loguru._logger import Logger


class KastaClient(BaseClient):
    log: Logger = LOG

    def __init__(self) -> None:
        self._tasks: set[asyncio.Task] = set()
        self._me: types.User | None = None
        super().__init__(
            PROJECT,
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
            session_string=Var.STRING_SESSION,
            workers=Var.WORKERS,
            workdir=DATA_DIR,
            plugins={"root": f"{PROJECT}.plugins", "exclude": []},
            parse_mode=enums.ParseMode.HTML,
            no_updates=False,
            skip_updates=True,
            sleep_threshold=15,
            max_concurrent_transmissions=1,
            max_message_cache_size=1000,
            protocol_factory=TCPAbridged,
        )

    def create_task(
        self,
        coro: Coroutine,
        *,
        catch: bool = False,
    ) -> asyncio.Task:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._task_done if catch else self._tasks.discard)
        return task

    def _task_done(self, task: asyncio.Task) -> None:
        self._tasks.discard(task)
        try:
            task.result()
        except asyncio.CancelledError:
            pass
        except Exception:
            self.log.exception("Background task failed")

    async def get_me(
        self,
        cache: bool = True,
    ) -> types.User:
        if cache and (me := self._me) is not None:
            return me
        me = await super().get_me()
        me.url = f"https://t.me/{me.username}" if me.username else f"tg://user?id={me.id}"
        if cache:
            self._me = me
        return me

    async def bootstrap(self) -> None:
        loop = asyncio.get_running_loop()
        stop = loop.create_future()
        signals = (signal.SIGINT, signal.SIGTERM, signal.SIGABRT)

        def _signal_handler(signum: int) -> None:
            sig_name = signal.Signals(signum).name
            self.log.warning(f"> STOP SIGNAL RECEIVED ({sig_name})")
            if not stop.done():
                stop.set_result(None)

        for sig in signals:
            loop.add_signal_handler(sig, _signal_handler, sig)
        try:
            await self.start()
            await stop
        finally:
            for sig in signals:
                loop.remove_signal_handler(sig)
            await self.stop()

    async def start(self) -> None:
        try:
            if not Var.API_ID:
                raise ValueError("Required: API_ID not set in .env")
            if not Var.API_HASH:
                raise ValueError("Required: API_HASH not set in .env")
            if not Var.STRING_SESSION:
                raise ValueError("Required: STRING_SESSION not set in .env")

            self.log.info("> 🚀 STARTING USERBOT...")
            if Var.DEV_MODE:
                await asyncio.sleep(random.uniform(3.5, 6.5))
            for attempt in range(1, 3 + 1):
                try:
                    await super().start()
                    break
                except (
                    errors.FloodWait,
                    errors.FloodPremiumWait,
                ) as fw:
                    amount = fw.value
                    if amount > 300:
                        self.log.error(f"> FLOOD WAIT TOO LONG ({amount}s)")
                        sys.exit(1)
                    self.log.warning(f"> FLOOD WAIT {amount}s ({attempt}/3)")
                    await asyncio.sleep(amount + random.uniform(10, 15))
            else:
                self.log.error("> START FAILED: FLOOD RETRIES EXHAUSTED")
                sys.exit(1)
        except Exception:
            self.log.exception("> USERBOT crashed during start")
            sys.exit(1)

        _me = [
            "> USERBOT DETAILS:",
            f"ID: {self.me.id}",
            f"First Name: {self.me.first_name}",
        ]
        if self.me.last_name:
            _me.append(f"Last Name: {self.me.last_name}")
        if self.me.username:
            _me.append(f"Username: @{self.me.username}")
        dc_id = self.me.dc_id or 0
        if dc_id:
            _me.append(f"DC: {dc_id}")
        self.log.info("\n".join(_me))

        self.create_task(self.__join_us())
        done = format_time(monotonic() - StartTime)
        launch = f"> 🚀 Userbot (DC{dc_id}) launched in {done}, layer: {layer}."
        await self.send_message("me", launch)
        self.log.success(f"> 🔥 USERBOT UP IN {done}.")
        Var.IS_STARTUP = True
        Var.STARTUP_EVENT.set()

    async def stop(self) -> None:
        if self._tasks:
            for task in self._tasks:
                task.cancel()
            try:
                await asyncio.wait_for(
                    asyncio.gather(
                        *self._tasks,
                        return_exceptions=True,
                    ),
                    timeout=5,
                )
            except TimeoutError:
                pass
        try:
            await super().stop()
            self.log.warning("> USERBOT STOPPED.")
        except Exception:
            pass

    async def __join_us(self) -> None:
        chat_id = -1004361705646
        try:
            peer = await self.resolve_peer(chat_id)
        except Exception:
            return
        try:
            await asyncio.sleep(random.uniform(3.5, 6.5))
            await self.invoke(JoinChannel(channel=peer))
        except Exception:
            pass
        try:
            await asyncio.sleep(random.uniform(1.5, 2.5))
            msgs = await self.invoke(
                GetHistory(
                    peer=peer,
                    offset_id=0,
                    offset_date=0,
                    add_offset=0,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
            if not msgs.messages:
                return
            message_id = msgs.messages[0].id
            await self.invoke(
                ReadHistory(
                    channel=peer,
                    max_id=message_id,
                )
            )
            await asyncio.sleep(random.uniform(1.5, 2.5))
            await self.invoke(
                GetMessagesViews(
                    peer=peer,
                    id=[message_id],
                    increment=True,
                )
            )
        except Exception:
            pass
