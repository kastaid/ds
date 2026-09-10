# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

from time import time
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import types

from ds.config import Var

from ._patching import patch, patchable

if TYPE_CHECKING:
    from pyrogram.client import Client

MAX_UPDATE_AGE = 3 * 60


@patch(pyrogram.handlers.handler.Handler)
class Handler:
    @patchable()
    async def check(
        self,
        client: Client,
        update: types.Update,
    ) -> bool:
        # startup queue handling
        if not Var.IS_STARTUP:
            await Var.STARTUP_EVENT.wait()

        # when skip_updates is disabled
        if not client.skip_updates and type(update) is types.Message:
            if getattr(update, "is_recovered", False):
                return False
            date = update.date
            if date is None:
                return False
            if (time() - date.timestamp()) > MAX_UPDATE_AGE:
                return False

        # fallback to normal handler flow
        return await self.old_check(client, update)
