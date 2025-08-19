# ds < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/ds/ >
# Please read the MIT License in
# < https://github.com/kastaid/ds/blob/main/LICENSE/ >.

import asyncio
from time import monotonic, time

from pyrogram import filters
from pyrogram.errors import RPCError, UsersTooMuch
from pyrogram.raw.functions import Ping
from pyrogram.raw.functions.messages import ReadMentions, ReadReactions

from ds import StartTime
from ds.config import Var
from ds.helpers import get_terminal_logs, restart, time_formatter
from ds.kasta import KastaClient


@KastaClient.on_message(
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
        f"🏓 Pong !!\n<b>Speed</b> – {end - start:.3f}s\n<b>Uptime</b> – {time_formatter((time() - StartTime) * 1000)}"
    )


@KastaClient.on_message(
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
    restart(update=True)


@KastaClient.on_message(
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
        await asyncio.sleep(1)
    await msg.delete()


@KastaClient.on_message(
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


@KastaClient.on_message(
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


@KastaClient.on_message(
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
            await asyncio.sleep(1)
    if len(chunk) > 0:
        try:
            await c.delete_messages(chat_id, chunk)
        except RPCError:
            pass
    await m.delete()


@KastaClient.on_message(
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
    await asyncio.gather(
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


@KastaClient.on_message(
    filters.command(
        "join",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & filters.reply
    & ~filters.forwarded
)
async def _join(c, m):
    """
    Join to the chat and retry when too much users
    Usage: join [reply (username/id)]
    """
    chat_id = m.reply_to_message.text
    if not chat_id:
        return
    if chat_id.isdecimal() or (chat_id.startswith("-") and chat_id[1:].isdecimal()):
        chat_id = int(chat_id)
    count, state = 0, False
    while True:
        try:
            state = bool(await c.join_chat(chat_id))
        except UsersTooMuch:
            count += 1
            await m.edit(rf"🔃 Join retry {count}...")
            await asyncio.sleep(6)
            continue
        except BaseException:
            break
        if state:
            break
    text = rf"✅ Joined as {count}." if state else r"❌ Error"
    await m.edit(text)


@KastaClient.on_message(
    filters.command(
        "leave",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & filters.reply
    & ~filters.forwarded
)
async def _leave(c, m):
    """
    Leave or delete to the chat
    Usage: leave [reply (username/id)]
    """
    chat_id = m.reply_to_message.text
    if not chat_id:
        return
    if chat_id.isdecimal() or (chat_id.startswith("-") and chat_id[1:].isdecimal()):
        chat_id = int(chat_id)
    state = False
    try:
        state = bool(await c.leave_chat(chat_id, delete=True))
    except BaseException:
        pass
    text = r"✅ Leaved" if state else r"❌ Error"
    await m.edit(text)


@KastaClient.on_message(
    filters.command(
        "kickme",
        prefixes=Var.HANDLER,
    )
    & filters.me
    & ~filters.forwarded
)
async def _kickme(c, m):
    """
    Leave or delete the current chat
    Usage: kickme
    """
    try:
        await c.leave_chat(m.chat.id, delete=True)
    except BaseException:
        pass
    await m.delete()
