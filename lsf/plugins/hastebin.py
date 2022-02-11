"""
The MIT License
Copyright 2022 Unknown
All Rights Reserved
"""
import requests

from ... import dispatcher
from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from ...handlers.valid import dev_plus, sudo_plus



@dev_plus
@sudo_plus
def haste(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text

    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]

    else:
        message.reply_text("What am I supposed to do with this?")
        return

    key = (
        requests.post("https://hastebin.com/documents", json={"content": data})
        .json()
        .get("result")
        .get("key")
    )

    url = f"https://hastebin.com/{key}"

    reply_text = f"Hastebin to *Haste* : {url}"

    message.reply_text(
        reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )

__mod_name__ = "HasteBin​"
