# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

from pyrogram import filters

from ds.config import Var
from ds.kasta import KastaClient


@KastaClient.on_message(filters.me, group=-100)
async def _watcher(_, m):  # noqa: RUF029
    if not Var.IS_STARTUP:
        m.stop_propagation()
