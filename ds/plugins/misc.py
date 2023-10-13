# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import sleep
from time import time, perf_counter
from pyrogram import filters
from pyrogram.types import Message
from .. import StartTime
from ..bot import User
from ..config import Var
from ..helpers import time_formatter, get_terminal_logs, restart


@User.on_message(
    filters.command(
        "ping",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def ping_(_, m: Message):
    start = perf_counter()
    msg = await m.edit("Ping !")
    pong = round(perf_counter() - start, 3)
    await msg.edit(
        "🏓 Pong !!\n<b>Speed</b> - <code>{}ms</code>\n<b>Uptime</b> - <code>{}</code>".format(
            pong,
            time_formatter((time() - StartTime) * 1000),
        ),
    )


@User.on_message(
    filters.command(
        "restart",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def restart_(_, m: Message):
    await m.edit("Restarting userbot...")
    restart()


@User.on_message(
    filters.command(
        "logs",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def logs_(_, m: Message):
    msg = await m.edit("Getting logs...")
    for count, file in enumerate(get_terminal_logs(), start=1):
        await m.reply_document(
            document=file,
            caption=f"Terminal Logs {count}",
            quote=False,
        )
        await sleep(1)
    await msg.delete()
