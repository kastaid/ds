# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import sleep
from typing import Set, Union
from pyrogram import filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from ..bot import User
from ..config import Var

DS_TASK: Set[int] = set()
DS1_TASK: Set[int] = set()
DS2_TASK: Set[int] = set()
DS3_TASK: Set[int] = set()
DS4_TASK: Set[int] = set()


@User.on_message(
    filters.command(
        [
            "ds",
            "ds1",
            "ds2",
            "ds3",
            "ds4",
        ],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def ds_(client: User, m: Message):
    chat_id = m.chat.id
    ds = m.command[0].lower()[2:3]
    text = "Please wait until previous •ds{}• finished or cancel it."
    if ds == "1":
        if chat_id in DS1_TASK:
            return await eor(m, text.format(ds), time=2)
    elif ds == "2":
        if chat_id in DS2_TASK:
            return await eor(m, text.format(ds), time=2)
    elif ds == "3":
        if chat_id in DS3_TASK:
            return await eor(m, text.format(ds), time=2)
    elif ds == "4":
        if chat_id in DS4_TASK:
            return await eor(m, text.format(ds), time=2)
    else:
        if chat_id in DS_TASK:
            return await eor(m, text.format(ds), time=2)
    if m.reply_to_message_id:
        try:
            args = m.command[1:]
            delay = float(args[0])
            count = int(args[1])
            message = m.reply_to_message
            await try_delete(m)
        except BaseException:
            return await eor(m, f"`{Var.HANDLER}ds{ds} [delay] [count] [reply]`", time=4)
    else:
        try:
            await try_delete(m)
            args = m.command[1:]
            delay = float(args[0])
            count = int(args[1])
            message = (
                m.text.markdown.replace(f"{Var.HANDLER}ds{ds}", "").replace(args[0], "").replace(args[1], "").strip()
            )
        except BaseException:
            return await eor(m, f"`{Var.HANDLER}ds{ds} [delay] [count] [text]`", time=4)
    delay = 2 if delay and int(delay) < 2 else delay
    if ds == "1":
        DS1_TASK.add(chat_id)
        for _ in range(count):
            if chat_id not in DS1_TASK:
                break
            try:
                await copy(message, chat_id, delay)
            except BaseException:
                break
        DS1_TASK.discard(chat_id)
    elif ds == "2":
        DS2_TASK.add(chat_id)
        for _ in range(count):
            if chat_id not in DS2_TASK:
                break
            try:
                await copy(message, chat_id, delay)
            except BaseException:
                break
        DS2_TASK.discard(chat_id)
    elif ds == "3":
        DS3_TASK.add(chat_id)
        for _ in range(count):
            if chat_id not in DS3_TASK:
                break
            try:
                await copy(message, chat_id, delay)
            except BaseException:
                break
        DS3_TASK.discard(chat_id)
    elif ds == "4":
        DS4_TASK.add(chat_id)
        for _ in range(count):
            if chat_id not in DS4_TASK:
                break
            try:
                await copy(message, chat_id, delay)
            except BaseException:
                break
        DS4_TASK.discard(chat_id)
    else:
        DS_TASK.add(chat_id)
        for _ in range(count):
            if chat_id not in DS_TASK:
                break
            try:
                await copy(message, chat_id, delay)
            except BaseException:
                break
        DS_TASK.discard(chat_id)


@User.on_message(
    filters.command(
        [
            "dscancel",
            "ds1cancel",
            "ds2cancel",
            "ds3cancel",
            "ds4cancel",
        ],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def dscancel_(_, m: Message):
    chat_id = m.chat.id
    ds = m.command[0].lower()[2:3].replace("c", "")
    text = "No current •ds{}• are running."
    if ds == "1":
        if chat_id not in DS1_TASK:
            return await eor(m, text.format(ds), time=2)
        DS1_TASK.discard(chat_id)
    elif ds == "2":
        if chat_id not in DS2_TASK:
            return await eor(m, text.format(ds), time=2)
        DS2_TASK.discard(chat_id)
    elif ds == "3":
        if chat_id not in DS3_TASK:
            return await eor(m, text.format(ds), time=2)
        DS3_TASK.discard(chat_id)
    elif ds == "4":
        if chat_id not in DS3_TASK:
            return await eor(m, text.format(ds), time=2)
        DS4_TASK.discard(chat_id)
    else:
        if chat_id not in DS_TASK:
            return await eor(m, text.format(ds), time=2)
        DS_TASK.discard(chat_id)
    await eor(m, f"`ds{ds} cancelled`", time=2)


@User.on_message(
    filters.command(
        [
            "dsstop",
            "ds1stop",
            "ds2stop",
            "ds3stop",
            "ds4stop",
        ],
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def dsstop_(_, m: Message):
    ds = m.command[0].lower()[2:3].replace("s", "")
    if ds == "1":
        DS1_TASK.clear()
    elif ds == "2":
        DS2_TASK.clear()
    elif ds == "3":
        DS3_TASK.clear()
    elif ds == "4":
        DS4_TASK.clear()
    else:
        DS_TASK.clear()
    await eor(m, f"`stopped all ds{ds}`", time=4)


@User.on_message(
    filters.command(
        "dsclear",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def dsclear_(_, m: Message):
    DS_TASK.clear()
    DS1_TASK.clear()
    DS2_TASK.clear()
    DS3_TASK.clear()
    DS4_TASK.clear()
    await eor(m, "`clear all ds*`", time=4)


async def copy(
    message: Union[Message, str],
    chat_id: int,
    time: Union[int, float],
) -> None:
    try:
        if isinstance(message, str):
            await User.send_message(
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
    except FloodWait as fw:
        await sleep(fw.value)
        await copy(message, chat_id, time)
    except BaseException:
        raise


async def eor(
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
    try:
        await sleep(time)
        return await msg.delete()
    except BaseException:
        return False


async def try_delete(message: Message) -> bool:
    try:
        return await message.delete()
    except BaseException:
        return False
