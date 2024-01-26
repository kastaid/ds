# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import sleep
from typing import Any, Tuple, Callable
import pyrogram
from pyrogram.errors import (
    FloodWait,
    PeerIdInvalid,
    UserIsBlocked,
    PersistentTimestampInvalid,
)
from ds.logger import LOG


def patch(obj: Any):
    def is_patchable(item: Tuple[str, Any]) -> bool:
        return getattr(item[1], "patchable", False)

    def wrapper(container: Callable) -> Callable:
        for name, func in filter(is_patchable, container.__dict__.items()):
            setattr(obj, f"old_{name}", getattr(obj, name, None))
            setattr(obj, name, func)
        return container

    return wrapper


def patchable(func: Callable) -> Callable:
    func.patchable = True
    return func


@patch(pyrogram.client.Client)
class Client:
    @patchable
    async def invoke(self, *args, **kwargs):
        try:
            return await self.old_invoke(*args, **kwargs)
        except FloodWait as fw:
            LOG.warning(fw)
            await sleep(fw.value)
            return await self.invoke(*args, **kwargs)
        except (
            UserIsBlocked,
            PersistentTimestampInvalid,
        ):
            pass

    @patchable
    async def resolve_peer(self, *args, **kwargs):
        try:
            return await self.old_resolve_peer(*args, **kwargs)
        except FloodWait as fw:
            LOG.warning(fw)
            await sleep(fw.value)
            return await self.resolve_peer(*args, **kwargs)
        except PeerIdInvalid:
            pass

    @patchable
    async def save_file(self, *args, **kwargs):
        try:
            return await self.old_save_file(*args, **kwargs)
        except FloodWait as fw:
            LOG.warning(fw)
            await sleep(fw.value)
            return await self.save_file(*args, **kwargs)
