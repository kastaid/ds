# Copyright (C) 2023-present kastaid
# This file is part of https://github.com/kastaid/ds
# Please read the MIT License at
# https://github.com/kastaid/ds/blob/main/LICENSE

from pyrogram import filters

from ds.config import Var
from ds.kasta import KastaClient


@KastaClient.on_message(filters.me, group=-100)
async def _watcher(_, m):  # noqa: RUF029
    if not Var.IS_STARTUP:
        m.stop_propagation()
