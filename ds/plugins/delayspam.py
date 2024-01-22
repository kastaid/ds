# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import sleep
from typing import Dict, Set, Union
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import RPCError, SlowmodeWait
from pyrogram.types import Message
from ds.config import Var
from ds.user import UserClient

DS_TASKS: Dict[int, Set[int]] = {i: set() for i in range(10)}


def get_task(ds: str) -> Set[int]:
    return DS_TASKS.get(int(ds or 0))


@UserClient.on_message(
    filters.command(
        [f"ds{i}" if i != 0 else "ds" for i in range(10)],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def ds_(c, m):
    """
    Start ds, ds1 - ds9
    Usage: ds [delay] [count] [text/reply]
    """
    chat_id = m.chat.id
    ds = m.command[0].lower()[2:3]
    task = get_task(ds)
    if chat_id in task:
        return await eor(c, m, f"Please wait until previous •ds{ds}• is finished or cancel it.", time=2)
    message = m.reply_to_message if m.reply_to_message_id else " ".join(m.text.markdown.split(" ")[3:])
    await c.try_delete(m)
    try:
        args = m.command[1:]
        delay, count = int(args[0]), int(args[1])
    except BaseException:
        return await eor(c, m, f"`{Var.HANDLER}ds{ds} [delay] [count] [text/reply]`", time=4)
    delay = 2 if int(delay) < 2 else delay
    task.add(chat_id)
    for _ in range(count):
        if chat_id not in get_task(ds):
            break
        try:
            await copy(c, message, chat_id, delay)
        except SlowmodeWait:
            pass
        except RPCError:
            break
    get_task(ds).discard(chat_id)


@UserClient.on_message(
    filters.command(
        [f"ds{i}cancel" if i != 0 else "dscancel" for i in range(10)],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def dscancel_(c, m):
    """
    Cancel ds - ds9 in current chat
    Usage: dscancel, ds1cancel
    """
    chat_id = m.chat.id
    ds = m.command[0].lower()[2:3].replace("c", "")
    task = get_task(ds)
    if chat_id not in task:
        return await eor(c, m, f"No running •ds{ds}• in current chat.", time=2)
    task.discard(chat_id)
    await eor(c, m, f"`cancelled ds{ds} in current chat`", time=2)


@UserClient.on_message(
    filters.command(
        [f"ds{i}stop" if i != 0 else "dsstop" for i in range(10)],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def dsstop_(c, m):
    """
    Stop ds - ds9 in all chats
    usage: dsstop, ds1stop
    """
    ds = m.command[0].lower()[2:3].replace("s", "")
    get_task(ds).clear()
    await eor(c, m, f"`stopped ds{ds} in all chats`", time=4)


@UserClient.on_message(
    filters.command(
        "dsclear",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def dsclear_(c, m):
    """
    Clear and stop all ds
    usage: dsclear
    """
    for task in DS_TASKS.values():
        task.clear()
    await eor(c, m, "`clear all ds*`", time=4)


async def copy(
    client,
    message: Union[str, Message],
    chat_id: int,
    time: Union[int, float],
) -> None:
    if isinstance(message, str):
        await client.send_message(
            chat_id,
            message,
            parse_mode=ParseMode.DEFAULT,
            disable_web_page_preview=True,
            disable_notification=True,
        )
    else:
        await message.copy(
            chat_id,
            parse_mode=ParseMode.DEFAULT,
            disable_notification=True,
            reply_to_message_id=None,
        )
    await sleep(time)


async def eor(
    client,
    message: Message,
    text: str,
    time: Union[int, float],
) -> Union[Message, bool]:
    try:
        msg = await message.edit(
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        if not time:
            return msg
    except BaseException:
        msg = await message.reply(
            text,
            quote=True,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            disable_notification=True,
        )
        if not time:
            return msg
    await sleep(time)
    return await client.try_delete(msg)
