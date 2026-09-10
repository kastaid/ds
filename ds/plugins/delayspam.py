# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio
import random
import re
from typing import TYPE_CHECKING

from pyrogram import (
    enums,
    errors,
    filters,
    types,
)

from ds.config import Var
from ds.helpers import (
    get_username,
    is_telegram_link,
    normalize_chat_id,
)
from ds.kasta import KastaClient

if TYPE_CHECKING:
    from pyrogram.types import Message

DS_RANGE = range(10)
DS_DELAY_MIN = 2
DS_RANDOM_THRESHOLD = 60
DS_RANDOM_DELAY = (3.5, 6.5)
DS_TASKS: dict[int, dict[int, asyncio.Task]] = {i: {} for i in DS_RANGE}
DS_ERROR_MAX = 3
TARGET_RE = re.compile(r"(?:^|\s+)to=(\S+)(?=\s|$)", re.IGNORECASE)
DEFAULT_PARSE_MODE = enums.ParseMode.DEFAULT
LINK_PREVIEW = types.LinkPreviewOptions(
    is_disabled=False,
    prefer_small_media=True,
    show_above_text=True,
)


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
    Usage: ds [delay] [count] [forward/fwd (reply only)] [text/reply] [to=chat]
    """
    chat_id, text = await parse_target(c, m, text=m.text.markdown)
    if chat_id is None:
        return await eor(m, "Invalid target chat.", time=3)
    ds = int(m.command[0].lower()[2:3] or 0)
    ds_name = get_ds_name(ds)
    task_store = get_task_store(ds)
    if chat_id in task_store:
        return await eor(m, f"Please wait, {ds_name} is running or cancel it.", time=3)
    await m.delete()
    args = text.split(maxsplit=3)
    try:
        delay, count = int(args[1]), int(args[2])
    except Exception:
        return await eor(
            m,
            f"`{Var.HANDLER}{ds_name} [delay] [count] [forward/fwd (reply only)] [text/reply] [to=chat]`",
            time=6,
        )
    is_text, is_forward = False, False
    from_chat_id = m.chat.id
    if m.reply_to_message_id:
        message = m.reply_to_message
        message_id = message.id
        is_forward = any(i in text.lower().split() for i in ("forward", "fwd"))
    else:
        message = args[3]
        message_id = 0
        is_text = True
    delay = max(DS_DELAY_MIN, delay)
    task = asyncio.create_task(
        run_ds(
            c,
            ds,
            chat_id,
            from_chat_id,
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
async def _dscancel(c, m):
    """
    Cancel ds - ds9 in target chat
    Usage: dscancel [to=chat], ds1cancel [to=chat]
    """
    chat_id, _ = await parse_target(c, m, text=" ".join(m.command[1:]))
    if chat_id is None:
        return await eor(m, "Invalid target chat.", time=3)
    ds = int(m.command[0].lower()[2:3].replace("c", "") or 0)
    ds_name = get_ds_name(ds)
    task_store = get_task_store(ds)
    if chat_id not in task_store:
        return await eor(m, f"No {ds_name} is running in target chat.", time=3)
    task = task_store.pop(chat_id)
    if not task.done():
        task.cancel()
    await eor(m, f"`canceled {ds_name} in target chat`", time=6)


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
    from_chat_id: int,
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
                from_chat_id,
                message_id,
                is_text,
                is_forward,
            )
            if is_forward:
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
    from_chat_id: int,
    message_id: int,
    is_text: bool,
    is_forward: bool,
) -> Message:
    if is_text:
        return await client.send_message(
            chat_id,
            message,
            parse_mode=DEFAULT_PARSE_MODE,
            disable_notification=True,
            link_preview_options=LINK_PREVIEW,
        )
    if is_forward:
        return await client.forward_messages(
            chat_id,
            from_chat_id=from_chat_id,
            message_ids=message_id,
            disable_notification=True,
        )
    if message.text:
        return await client.send_message(
            chat_id,
            message.text,
            entities=message.entities,
            parse_mode=enums.ParseMode.DISABLED,
            disable_notification=True,
            link_preview_options=message.link_preview_options,
        )
    return await client.copy_message(
        chat_id,
        from_chat_id=from_chat_id,
        message_id=message_id,
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
            parse_mode=DEFAULT_PARSE_MODE,
            link_preview_options=types.LinkPreviewOptions(is_disabled=True),
        )
        if not time:
            return result
    except Exception:
        try:
            result = await message.reply(
                text,
                parse_mode=DEFAULT_PARSE_MODE,
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


async def parse_target(
    client: KastaClient,
    message: Message,
    *,
    text: str,
) -> tuple[int | None, str]:
    match = TARGET_RE.search(text)
    target = match.group(1) if match else None
    if match:
        text = text[: match.start()] + text[match.end() :]
    if not target:
        return message.chat.id, text
    chat_id = normalize_chat_id(target)
    if isinstance(chat_id, int):
        return chat_id, text
    if is_telegram_link(chat_id):
        chat_id = get_username(chat_id)
    try:
        chat = await client.get_chat(chat_id)
        return chat.id, text
    except Exception:
        return None, text
