"""
The MIT License
Copyright 2022 Unknown
All Rights Reserved
"""
import socket
import asyncio
import os
import re
import aiofiles
import sys
import traceback

from functools import partial, wraps
from pykeyboard import InlineKeyboard

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

from lsf import aiohttpsession as index
from lsf import LOGGER, xx



def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line

    result.append(small_msg)

    return result


def greatest(func):
    @wraps(func)
    async def metaverse(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await xx.leave_chat(message.chat.id)
            return
        except Exception as master:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for a in error_feedback:
                await xx.send_message(LOGGER, a)
            raise master

    return metaverse


def portable(host, port, content):
    go = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    go.connect((host, port))
    go.sendall(content.encode())
    go.shutdown(socket.SHUT_WR)
    while True:
        data = go.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    go.close()


async def paste_bin(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(None, partial(portable, "ezup.dev", 9999, content))
    return link


pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


async def preview_str(preview: str) -> bool:
    for _ in range(7):
        try:
            async with index.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False


@xx.on_message(filters.command("pasbin") & ~filters.edited)
@greatest
async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message With /paste")
    m = await message.reply_text("Pasting...")
    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)
    elif message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.file_size > 1048576:
            return await m.edit("You can only paste files smaller than 1MB.")
        if not pattern.search(document.mime_type):
            return await m.edit("Only text files can be pasted.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = await paste_bin(content)
    preview = link + "/preview.png"
    button = InlineKeyboard(row_width=1)
    button.add(InlineKeyboardButton(text="Paste-Bin", url=link))

    if await preview_str(preview):
        try:
            await message.reply_photo(photo=preview, quote=False, reply_markup=button)
            return await m.delete()
        except Exception:
            pass
    return await m.edit(link)
