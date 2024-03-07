# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

from asyncio import sleep, gather
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
async def _ping(c, m):
    """
    Ping Telegram server
    Usage: ping
    """
    start = monotonic()
    try:
        await c.invoke(Ping(ping_id=0))
        msg = m
    except RPCError:
        msg = await m.edit("Ping !")
    end = monotonic()
    await msg.edit(
        f"🏓 Pong !!\n<b>Speed</b> - <code>{end - start:.3f}s</code>\n<b>Uptime</b> - <code>{time_formatter((time() - StartTime) * 1000)}</code>"
    )


@UserClient.on_message(
    filters.command(
        "restart",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _restart(_, m):
    """
    Restart userbot
    Usage: restart
    """
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
async def _logs(_, m):
    """
    Get the logs
    Usage: logs
    """
    msg = await m.edit("Getting logs...")
    for count, file in enumerate(get_terminal_logs(), start=1):
        await m.reply_document(
            document=file,
            caption=f"Terminal Logs {count}",
            quote=False,
        )
        await sleep(1)
    await msg.delete()


@UserClient.on_message(
    filters.command(
        "id",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _id(_, m):
    """
    Get user id
    Usage: id
    """
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
async def _del(_, m):
    """
    Delete message
    Usage: del
    """
    await m.delete()
    if m.reply_to_message_id:
        await m.reply_to_message.delete()


@UserClient.on_message(
    filters.command(
        "purge",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & filters.reply
    & ~filters.forwarded
)
async def _purge(c, m):
    """
    Purge urself by reply
    Usage: purge
    """
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
    await m.delete()


@UserClient.on_message(
    filters.command(
        "read",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _read(c, m):
    """
    Read chat current chat also mentions and reactions
    Usage: read
    """
    chat_id = m.chat.id
    try:
        peer = await c.resolve_peer(chat_id)
    except RPCError:
        return
    await gather(
        *[
            c.invoke(i)
            for i in (
                ReadMentions(peer=peer),
                ReadReactions(peer=peer),
            )
        ],
    )
    try:
        await c.read_chat_history(chat_id)
    except RPCError:
        pass
    await m.delete()
