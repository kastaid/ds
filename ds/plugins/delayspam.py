# Copyright (C) 2023-present kastaid
# https://github.com/kastaid/ds
# MIT License

import asyncio

from pyrogram import errors, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from ds.config import Var
from ds.kasta import KastaClient

DS_TASKS: dict[int, dict[int, asyncio.Task]] = {i: {} for i in range(10)}


def get_task_store(ds: int) -> dict[int, asyncio.Task]:
    return DS_TASKS.get(ds)


@KastaClient.on_message(
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
    ds = int(cmd[0].lower()[2:3] or 0)
    task_store = get_task_store(ds)
    if chat_id in task_store:
        return await eor(m, f"Please wait until previous •ds{ds}• is finished or cancel it.", time=6)
    await m.delete()
    try:
        args = cmd[1:]
        delay, count = int(args[0]), int(args[1])
    except BaseException:
        return await eor(m, f"`{Var.HANDLER}ds{ds} [delay] [count] [forward (reply only)] [text/reply]`", time=6)
    is_text, is_forward = False, False
    if m.reply_to_message_id:
        message = m.reply_to_message
        message_id = message.id
        is_forward = "forward" in m.text.lower()
    else:
        message = " ".join(m.text.markdown.split(" ")[3:])
        message_id = 0
        is_text = True
    delay = max(2, delay)
    task = asyncio.create_task(
        run_delayspam(
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
    task.add_done_callback(lambda t, k=chat_id: get_task_store(ds).pop(k, None))


@KastaClient.on_message(
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
    ds = int(m.command[0].lower()[2:3].replace("c", "") or 0)
    task_store = get_task_store(ds)
    if chat_id not in task_store:
        return await eor(m, f"No running •ds{ds}• in current chat.", time=6)
    task = task_store.pop(chat_id)
    if not task.done():
        task.cancel()
    await eor(m, f"`canceled ds{ds} in current chat`", time=6)


@KastaClient.on_message(
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
    ds = int(m.command[0].lower()[2:3].replace("s", "") or 0)
    task_store = get_task_store(ds)
    for task in list(task_store.values()):
        if not task.done():
            task.cancel()
    task_store.clear()
    await eor(m, f"`stopped ds{ds} in all chats`", time=0)


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
    await eor(m, "`clear all ds*`", time=0)


async def run_delayspam(
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
    for _ in range(count):
        if chat_id not in get_task_store(ds):
            break
        try:
            await asyncio.sleep(1)
            result = await send_message(
                client,
                message,
                chat_id,
                message_id,
                delay,
                is_forward,
            )
            if not is_text:
                message_id = getattr(result, "id", message_id)
        except errors.RPCError:
            pass
        except Exception as err:
            client.log.error(err)
            client.log.exception(err)
            if chat_id not in Var.ERROR_RETRY:
                Var.ERROR_RETRY.update({chat_id: 1})
            else:
                Var.ERROR_RETRY.update({chat_id: Var.ERROR_RETRY[chat_id] + 1})
            if chat_id in Var.ERROR_RETRY and Var.ERROR_RETRY[chat_id] > 3:
                Var.ERROR_RETRY.pop(chat_id)
                break


async def send_message(
    client: KastaClient,
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
    await asyncio.sleep(delay)
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
    await asyncio.sleep(time)
    return await result.delete()
