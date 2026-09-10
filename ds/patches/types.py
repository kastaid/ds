# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import pyrogram

from ._patching import patch, patchable


@patch(pyrogram.types.messages_and_media.message.Message)
class Message:
    @patchable()
    async def delete(
        self,
        *args,
        **kwargs,
    ) -> bool:
        try:
            return bool(await self.old_delete(*args, **kwargs))
        except Exception:
            return False
