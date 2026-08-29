# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio
import random
from typing import TYPE_CHECKING

from pyrogram import (
    enums,
    errors,
    filters,
)

from ds.config import Var
from ds.kasta import KastaClient

if TYPE_CHECKING:
    from pyrogram.types import Message

DS_RANGE = range(10)
DS_DELAY_MIN = 2
DS_RANDOM_THRESHOLD = 60
DS_RANDOM_DELAY = (3.5, 6.5)
DS_TASKS: dict[int, dict[int, asyncio.Task]] = {i: {} for i in DS_RANGE}
DS_ERROR_MAX = 3


@KastaClient.on_message(
    filters.command(
        [f"ds{i}" if i else "ds" for i in DS_RANGE],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _ds(c, m):
    """
    Start ds, ds1 - ds9
    Usage: ds [delay] [count] [forward (reply only)] [text/reply]
    """
    chat_id = m.chat.id
    cmd = m.command
    ds = int(cmd[0].lower()[2:3] or 0)
    ds_name = get_ds_name(ds)
    task_store = get_task_store(ds)
    if chat_id in task_store:
        return await eor(m, f"Please wait, {ds_name} is running or cancel it.", time=3)
    await m.delete()
    try:
        args = cmd[1:]
        delay, count = int(args[0]), int(args[1])
    except Exception:
        return await eor(m, f"`{Var.HANDLER}{ds_name} [delay] [count] [forward (reply only)] [text/reply]`", time=6)
    is_text, is_forward = False, False
    if m.reply_to_message_id:
        message = m.reply_to_message
        message_id = message.id
        is_forward = "forward" in m.text.lower()
    else:
        message = " ".join(m.text.markdown.split(" ")[3:])
        message_id = 0
        is_text = True
    delay = max(DS_DELAY_MIN, delay)
    task = asyncio.create_task(
        run_ds(
            c,
            ds,
            chat_id,
            message,
            message_id,
            delay,
            count,
            is_text,
            is_forward,
        )
    )
    DS_TASKS[ds][chat_id] = task
    task.add_done_callback(lambda _, k=chat_id: get_task_store(ds).pop(k, None))


@KastaClient.on_message(
    filters.command(
        [f"ds{i}cancel" if i else "dscancel" for i in DS_RANGE],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _dscancel(_, m):
    """
    Cancel ds - ds9 in current chat
    Usage: dscancel, ds1cancel
    """
    chat_id = m.chat.id
    ds = int(m.command[0].lower()[2:3].replace("c", "") or 0)
    ds_name = get_ds_name(ds)
    task_store = get_task_store(ds)
    if chat_id not in task_store:
        return await eor(m, f"No {ds_name} is running in current chat.", time=3)
    task = task_store.pop(chat_id)
    if not task.done():
        task.cancel()
    await eor(m, f"`canceled {ds_name} in current chat`", time=6)


@KastaClient.on_message(
    filters.command(
        [f"ds{i}stop" if i else "dsstop" for i in DS_RANGE],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _dsstop(_, m):
    """
    Stop ds - ds9 in all chats
    usage: dsstop, ds1stop
    """
    ds = int(m.command[0].lower()[2:3].replace("s", "") or 0)
    ds_name = get_ds_name(ds)
    task_store = get_task_store(ds)
    for task in list(task_store.values()):
        if not task.done():
            task.cancel()
    task_store.clear()
    await eor(m, f"`stopped {ds_name} in all chats`")


@KastaClient.on_message(
    filters.command(
        "dsclear",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _dsclear(_, m):
    """
    Clear and stop all ds
    usage: dsclear
    """
    for store in DS_TASKS.values():
        for task in list(store.values()):
            if not task.done():
                task.cancel()
        store.clear()
    await eor(m, "`clear all ds*`")


def get_ds_name(ds: int) -> str:
    return f"ds{ds}" if ds else "ds"


def get_task_store(ds: int) -> dict[int, asyncio.Task]:
    return DS_TASKS.get(ds)


async def run_ds(
    client: KastaClient,
    ds: int,
    chat_id: int,
    message: Message | str,
    message_id: int,
    delay: int,
    count: int,
    is_text: bool,
    is_forward: bool,
) -> None:
    error_count = 0
    for _ in range(count):
        if chat_id not in get_task_store(ds):
            break
        try:
            if delay > DS_RANDOM_THRESHOLD:
                await asyncio.sleep(random.uniform(*DS_RANDOM_DELAY))
            result = await send_ds_message(
                client,
                message,
                chat_id,
                message_id,
                is_text,
                is_forward,
            )
            if not is_text:
                message_id = getattr(result, "id", message_id)
            error_count = 0
            await asyncio.sleep(delay)
        except errors.SlowmodeWait as err:
            client.log.warning(f"Delayspam {get_ds_name(ds)} slowmode wait: {err.value}s")
            await asyncio.sleep(err.value + 5)
        except (
            errors.FloodWait,
            errors.FloodPremiumWait,
        ) as err:
            wait = err.value + random.uniform(15, 30)
            client.log.warning(f"Delayspam {get_ds_name(ds)} flood wait: {err.value}s, sleeping {wait:.1f}s")
            await asyncio.sleep(wait)
        except (
            errors.ChannelInvalid,
            errors.ChannelPrivate,
            errors.ChatWriteForbidden,
            errors.ChatSendPhotosForbidden,
            errors.ChatSendVideosForbidden,
            errors.ChatSendGifsForbidden,
            errors.ChatSendVoicesForbidden,
            errors.ChatSendAudiosForbidden,
            errors.ChatSendMediaForbidden,
        ) as err:
            client.log.warning(f"Delayspam {get_ds_name(ds)} stopped in chat {chat_id}: {err}")
            break
        except Exception as err:
            error_count += 1
            if error_count > DS_ERROR_MAX:
                client.log.warning(
                    f"Delayspam {get_ds_name(ds)} stopped after {error_count} errors in chat {chat_id}: {err}"
                )
                break


async def send_ds_message(
    client: KastaClient,
    message: str | Message,
    chat_id: int,
    message_id: int,
    is_text: bool,
    is_forward: bool,
) -> Message:
    if is_text:
        return await client.send_message(
            chat_id,
            message,
            parse_mode=enums.ParseMode.DEFAULT,
            disable_notification=True,
        )
    if is_forward:
        return await client.forward_messages(
            chat_id,
            from_chat_id=chat_id,
            message_ids=message_id,
            disable_notification=True,
        )
    return await client.copy_message(
        chat_id,
        from_chat_id=chat_id,
        message_id=message_id,
        parse_mode=enums.ParseMode.DEFAULT,
        disable_notification=True,
    )


async def eor(
    message: Message,
    text: str,
    *,
    time: float = 0,
) -> Message | bool | None:
    result = None
    try:
        result = await message.edit(
            text,
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        if not time:
            return result
    except Exception:
        try:
            result = await message.reply(
                text,
                quote=True,
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_notification=True,
            )
            if not time:
                return result
        except Exception:
            pass
    if result:
        await asyncio.sleep(time)
        result = await result.delete()
    return result
