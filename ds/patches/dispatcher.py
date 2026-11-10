# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio
import inspect
import logging

import pyrogram
from pyrogram.handlers import ErrorHandler, RawUpdateHandler

from ._patching import patch, patchable

log = logging.getLogger(__name__)


@patch(pyrogram.dispatcher.Dispatcher)
class Dispatcher:
    @patchable()
    async def handler_worker(self) -> None:
        while True:
            packet = await self.updates_queue.get()
            if packet is None:
                break

            try:
                update, users, chats = packet
                parser = self.update_parsers.get(type(update), None)

                parsed_update, handler_type = (
                    await parser(update, users, chats) if parser is not None else (None, type(None))
                )

                if parsed_update is not None and getattr(update, "pts_count", None) == -1:
                    parsed_update.is_recovered = True

                for group in self.groups.values():
                    for handler in group:
                        if isinstance(handler, ErrorHandler):
                            continue

                        args = None
                        if isinstance(handler, handler_type):
                            try:
                                if not await handler.check(self.client, parsed_update):
                                    continue
                                args = (parsed_update,)
                            except Exception:
                                log.exception("Failed to check handler filters")
                                continue
                        elif isinstance(handler, RawUpdateHandler):
                            try:
                                if not await handler.check(self.client, update):
                                    continue
                                args = (update, users, chats)
                            except Exception:
                                log.exception("Failed to check raw update handler filters")
                                continue
                        else:
                            continue

                        callback = handler.callback
                        try:
                            if inspect.iscoroutinefunction(callback):
                                await callback(self.client, *args)
                            else:
                                await asyncio.get_running_loop().run_in_executor(
                                    self.client.executor,
                                    callback,
                                    self.client,
                                    *args,
                                )
                        except pyrogram.StopPropagation:
                            raise
                        except pyrogram.ContinuePropagation:
                            continue
                        except Exception as e:
                            await self.handle_update_handler_exception(
                                e,
                                handler,
                                update,
                                users,
                                chats,
                            )

                        break
            except pyrogram.StopPropagation:
                pass
            except Exception:
                log.exception("Failed to process update in handler_worker")
