# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

from collections.abc import Callable
from contextlib import (
    asynccontextmanager,
    contextmanager,
)
from inspect import isasyncgenfunction
from typing import Any

import pyrogram.client
import pyrogram.errors
import pyrogram.types.messages_and_media.message

type Decorator[T] = Callable[[type[T]], type[T]]
type AnyCallable = Callable[..., Any]


def patch[T](target: type[Any]) -> Decorator[T]:
    def wrapper(container: type[T]) -> type[T]:
        for name, func in container.__dict__.items():
            if not getattr(func, "patchable", False):
                continue

            old = getattr(target, name, None)
            if old is not None:
                setattr(target, f"old_{name}", old)

            if func.is_property:
                patched = property(func)
            elif func.is_static:
                patched = staticmethod(func)
            elif func.is_context:
                patched = asynccontextmanager(func) if isasyncgenfunction(func) else contextmanager(func)
            else:
                patched = func

            setattr(target, name, patched)

        return container

    return wrapper


def patchable(
    is_property: bool = False,
    is_static: bool = False,
    is_context: bool = False,
) -> Callable[[AnyCallable], AnyCallable]:
    def wrapper(func: AnyCallable) -> AnyCallable:
        func.patchable = True
        func.is_property = is_property
        func.is_static = is_static
        func.is_context = is_context
        return func

    return wrapper


@patch(pyrogram.client.Client)
class Client:
    @patchable()
    async def invoke(self, *args, **kwargs):
        try:
            return await self.old_invoke(*args, **kwargs)
        except (
            TimeoutError,
            pyrogram.errors.UserIsBlocked,
            pyrogram.errors.PersistentTimestampInvalid,
        ):
            pass


@patch(pyrogram.types.messages_and_media.message.Message)
class Message:
    @patchable(True)
    def client(self) -> Client:
        return self._client

    @patchable()
    async def delete(self, revoke: bool = True) -> bool:
        try:
            return await self.old_delete(revoke=revoke)
        except Exception:
            return False
