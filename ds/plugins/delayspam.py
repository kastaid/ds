# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import sleep
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import RPCError
from pyrogram.types import Message
from ds.config import Var
from ds.user import UserClient


def get_task(ds: str) -> set[int]:
    return Var.DS_TASKS.get(int(ds or 0))


@UserClient.on_message(
    filters.command(
        [f"ds{i}" if i != 0 else "ds" for i in range(10)],
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
    ds = cmd[0].lower()[2:3]
    task = get_task(ds)
    if chat_id in task:
        return await eor(m, f"Please wait until previous •ds{ds}• is finished or cancel it.", time=2)
    await m.delete()
    try:
        args = cmd[1:]
        delay, count = int(args[0]), int(args[1])
    except BaseException:
        return await eor(m, f"`{Var.HANDLER}ds{ds} [delay] [count] [forward (reply only)] [text/reply]`", time=4)
    is_text, is_forward = False, False
    if m.reply_to_message_id:
        message = m.reply_to_message
        message_id = message.id
        is_forward = "forward" in m.text.lower()
    else:
        message = " ".join(m.text.markdown.split(" ")[3:])
        message_id = 0
        is_text = True
    delay = 2 if int(delay) < 2 else delay
    task.add(chat_id)
    for _ in range(count):
        if chat_id not in get_task(ds):
            break
        try:
            await sleep(0.5)
            result = await send_message(
                c,
                message,
                chat_id,
                message_id,
                delay,
                is_forward,
            )
            if not is_text:
                message_id = getattr(result, "id", message_id)
        except RPCError:
            pass
        except Exception as err:
            c.log.error(err)
            c.log.exception(err)
            if chat_id not in Var.ERROR_RETRY:
                Var.ERROR_RETRY.update({chat_id: 1})
            else:
                Var.ERROR_RETRY.update({chat_id: Var.ERROR_RETRY[chat_id] + 1})
            if chat_id in Var.ERROR_RETRY and Var.ERROR_RETRY[chat_id] > 3:
                Var.ERROR_RETRY.pop(chat_id)
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
async def _dscancel(_, m):
    """
    Cancel ds - ds9 in current chat
    Usage: dscancel, ds1cancel
    """
    chat_id = m.chat.id
    ds = m.command[0].lower()[2:3].replace("c", "")
    task = get_task(ds)
    if chat_id not in task:
        return await eor(m, f"No running •ds{ds}• in current chat.", time=2)
    task.discard(chat_id)
    await eor(m, f"`cancelled ds{ds} in current chat`", time=2)


@UserClient.on_message(
    filters.command(
        [f"ds{i}stop" if i != 0 else "dsstop" for i in range(10)],
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
    ds = m.command[0].lower()[2:3].replace("s", "")
    get_task(ds).clear()
    await eor(m, f"`stopped ds{ds} in all chats`", time=4)


@UserClient.on_message(
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
    for task in Var.DS_TASKS.values():
        task.clear()
    await eor(m, "`clear all ds*`", time=4)


async def send_message(
    client: UserClient,
    message: str | Message,
    chat_id: int,
    message_id: int,
    delay: int | float,
    is_forward: bool,
) -> Message:
    if isinstance(message, str):
        result = await client.send_message(
            chat_id,
            message,
            parse_mode=ParseMode.DEFAULT,
            disable_notification=True,
        )
    else:
        if is_forward:
            result = await client.forward_messages(
                chat_id,
                from_chat_id=chat_id,
                message_ids=message_id,
                disable_notification=True,
            )
        else:
            result = await client.copy_message(
                chat_id,
                from_chat_id=chat_id,
                message_id=message_id,
                parse_mode=ParseMode.DEFAULT,
                disable_notification=True,
            )
    await sleep(delay)
    return result


async def eor(
    message: Message,
    text: str,
    time: int | float,
) -> Message | bool:
    try:
        result = await message.edit(
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        if not time:
            return result
    except BaseException:
        result = await message.reply(
            text,
            quote=True,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            disable_notification=True,
        )
        if not time:
            return result
    await sleep(time)
    return await result.delete()
