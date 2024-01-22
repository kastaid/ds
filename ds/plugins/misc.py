# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import sleep
from time import time, monotonic
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.raw.functions import Ping
from pyrogram.raw.functions.messages import ReadMentions, ReadReactions
from ds import StartTime
from ds.config import Var
from ds.helpers import time_formatter, get_terminal_logs, restart
from ds.user import UserClient


@UserClient.on_message(
    filters.command(
        "ping",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def ping_(c, m):
    start = monotonic()
    try:
        await c.invoke(Ping(ping_id=0))
        msg = m
    except RPCError:
        msg = await m.edit("Ping !")
    end = monotonic()
    await msg.edit(
        "🏓 Pong !!\n<b>Speed</b> - <code>{:.3f}s</code>\n<b>Uptime</b> - <code>{}</code>".format(
            end - start,
            time_formatter((time() - StartTime) * 1000),
        ),
    )


@UserClient.on_message(
    filters.command(
        "restart",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def restart_(_, m):
    await m.edit("Restarting Userbot...")
    restart()


@UserClient.on_message(
    filters.command(
        "logs",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def logs_(c, m):
    msg = await m.edit("Getting logs...")
    for count, file in enumerate(get_terminal_logs(), start=1):
        await m.reply_document(
            document=file,
            caption=f"Terminal Logs {count}",
            quote=False,
        )
        await sleep(1)
    await c.try_delete(msg)


@UserClient.on_message(
    filters.command(
        "id",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def id_(_, m):
    who = m.reply_to_message.from_user.id if m.reply_to_message_id else m.chat.id
    await m.edit(f"<code>{who}</code>")


@UserClient.on_message(
    filters.command(
        "del",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def del_(c, m):
    await c.try_delete(m)
    if m.reply_to_message_id:
        await c.try_delete(m.reply_to_message)


@UserClient.on_message(
    filters.command(
        "purge",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & filters.reply
    & ~filters.forwarded
)
async def purge_(c, m):
    chunk = []
    chat_id, reply_id = m.chat.id, m.reply_to_message.id
    async for msg in c.get_chat_history(
        chat_id=chat_id,
        limit=m.id - reply_id + 1,
    ):
        if msg.id < reply_id:
            break
        if msg.from_user.id != c.me.id:
            continue
        chunk.append(msg.id)
        if len(chunk) >= 100:
            try:
                await c.delete_messages(chat_id, chunk)
            except RPCError:
                pass
            chunk.clear()
            await sleep(1)
    if len(chunk) > 0:
        try:
            await c.delete_messages(chat_id, chunk)
        except RPCError:
            pass
    await c.try_delete(m)


@UserClient.on_message(
    filters.command(
        "read",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def read_(c, m):
    try:
        peer = await c.resolve_peer(m.chat.id)
    except RPCError:
        return
    try:
        await c.invoke(ReadMentions(peer=peer))
        await sleep(1)
    except RPCError:
        pass
    try:
        await c.invoke(ReadReactions(peer=peer))
    except RPCError:
        pass
    await c.try_delete(m)
