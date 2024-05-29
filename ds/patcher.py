# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import logging
from asyncio import sleep
from collections.abc import Callable
from functools import wraps
from random import randrange
from typing import Any, T
import pyrogram.client
import pyrogram.errors
import pyrogram.types.messages_and_media.message
from .logger import LOG


def patch(target: Any):
    def is_patchable(item: tuple[str, Any]) -> bool:
        return getattr(item[1], "patchable", False)

    @wraps(target)
    def wrapper(container: type[T]) -> T:
        for name, func in filter(is_patchable, container.__dict__.items()):
            old = getattr(target, name, None)
            if old is not None:
                setattr(target, f"old_{name}", old)
            if getattr(func, "is_property", False):
                func = property(func)
            setattr(target, name, func)
        return container

    return wrapper


def patchable(is_property: bool = False) -> Callable:
    def wrapper(func: Callable) -> Callable:
        func.patchable = True
        func.is_property = is_property
        return func

    return wrapper


@patch(pyrogram.client.Client)
class Client:
    @patchable(True)
    def log(self) -> logging:
        return LOG

    @patchable()
    async def invoke(self, *args, **kwargs):
        try:
            return await self.old_invoke(*args, **kwargs)
        except pyrogram.errors.FloodWait as fw:
            self.log.warning(fw)
            sec = fw.value + randrange(5, 15)
            await sleep(sec)
            return await self.invoke(*args, **kwargs)
        except (
            TimeoutError,
            pyrogram.errors.UserIsBlocked,
            pyrogram.errors.PersistentTimestampInvalid,
        ):
            pass

    @patchable()
    async def resolve_peer(self, *args, **kwargs):
        try:
            return await self.old_resolve_peer(*args, **kwargs)
        except pyrogram.errors.FloodWait as fw:
            self.log.warning(fw)
            sec = fw.value + randrange(5, 15)
            await sleep(sec)
            return await self.resolve_peer(*args, **kwargs)
        except pyrogram.errors.PeerIdInvalid:
            pass

    @patchable()
    async def save_file(self, *args, **kwargs):
        try:
            return await self.old_save_file(*args, **kwargs)
        except pyrogram.errors.FloodWait as fw:
            self.log.warning(fw)
            sec = fw.value + randrange(5, 15)
            await sleep(sec)
            return await self.save_file(*args, **kwargs)


@patch(pyrogram.types.messages_and_media.message.Message)
class Message:
    @patchable(True)
    def client(self) -> Client:
        return self._client

    @patchable()
    async def delete(self, revoke: bool = True) -> bool:
        try:
            return await self.old_delete(revoke=revoke)
        except BaseException:
            return False
