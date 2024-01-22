from asyncio import sleep
import pyrogram
from pyrogram.errors.exceptions.flood_420 import FloodWait
from ds.logger import LOG


def patch(obj):
    def is_patchable(item):
        return getattr(item[1], "patchable", False)

    def wrapper(container):
        for name, func in filter(is_patchable, container.__dict__.items()):
            setattr(obj, f"old_{name}", getattr(obj, name, None))
            setattr(obj, name, func)
        return container

    return wrapper


def patchable(func):
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

    @patchable
    async def resolve_peer(self, *args, **kwargs):
        try:
            return await self.old_resolve_peer(*args, **kwargs)
        except FloodWait as fw:
            LOG.warning(fw)
            await sleep(fw.value)
            return await self.resolve_peer(*args, **kwargs)

    @patchable
    async def save_file(self, *args, **kwargs):
        try:
            return await self.old_save_file(*args, **kwargs)
        except FloodWait as fw:
            LOG.warning(fw)
            await sleep(fw.value)
            return await self.save_file(*args, **kwargs)
