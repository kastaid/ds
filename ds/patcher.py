# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio
import random
from typing import TYPE_CHECKING, Any

import pyrogram.client
import pyrogram.errors
import pyrogram.types.messages_and_media.message

if TYPE_CHECKING:
    from collections.abc import Callable


def patch[T](target: Any) -> Callable[[type[T]], type[T]]:
    def is_patchable(item: tuple[str, Any]) -> bool:
        return getattr(item[1], "patchable", False)

    def wrapper(container: type[T]) -> type[T]:
        for name, func in filter(is_patchable, container.__dict__.items()):
            old = getattr(target, name, None)
            if old is not None:
                setattr(target, f"old_{name}", old)
            if getattr(func, "is_property", False):
                setattr(target, name, property(func))
            else:
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
    @patchable()
    async def invoke(self, *args, **kwargs):
        try:
            return await self.old_invoke(*args, **kwargs)
        except pyrogram.errors.FloodWait as fw:
            self.log.warning(fw)
            await asyncio.sleep(fw.value + random.uniform(10, 15))
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
            await asyncio.sleep(fw.value + random.uniform(10, 15))
            return await self.resolve_peer(*args, **kwargs)
        except pyrogram.errors.PeerIdInvalid:
            pass

    @patchable()
    async def save_file(self, *args, **kwargs):
        try:
            return await self.old_save_file(*args, **kwargs)
        except pyrogram.errors.FloodWait as fw:
            self.log.warning(fw)
            await asyncio.sleep(fw.value + random.uniform(10, 15))
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
