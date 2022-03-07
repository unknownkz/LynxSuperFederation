# @unknownkz

import numpy as np

from base64 import b64decode
from time import sleep
from random import randrange

from ... import LOGGER
from ...database import users_sql as sql
from ...handlers.valid import is_user_admin, bot_admin as absolute
from ...handlers.decorators import Lynxcmd
from . import LIST_NOSPAM, Weird

from telegram import Update, Message
from telegram.error import (
    BadRequest,
    TelegramError,
    ChatMigrated,
)

from telegram.ext import (
    CallbackContext,
    Filters,
    CommandHandler,
    run_async,
)


CHAT_GROUP = 30


@Lynxcmd("bcast", group=CHAT_GROUP)
@absolute
def broadcasts(update: Update, context: CallbackContext):
    wx = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    xx = is_user_admin(chat, user.id)
    if not xx:
        wx.reply_text(
            "Only admins can do this."
        )
        return xx
    succ = 0
    chats = sql.get_all_chats(chat_id)
    chats = chats.append(LIST_NOSPAM)
    np.array(chats.chat_id, dtype=str)
    to_send = wx.text.split(None, 1)
    to_group = True if chat_id in chats == LIST_NOSPAM or Weird else False
    if len(to_send) >= 2:
       to_group = False
       failed = 0
       for xz in chats not in LIST_NOSPAM or Weird:
           try:
               context.bot.sendMessage(
                   xz.chat_id,
                   to_send[1],
                   parse_mode="MARKDOWN",
                   disable_web_page_preview=True,
               )
               sleep(randrange(2, 4))
               succ += 1
           except (ChatMigrated, TelegramError, BadReauest) as excp:
               failed += 1
               escp = get_exception(excp)
               if escp == "An unknown error occurred":
                   try:
                       context.bot.sendMessage(
                           xz.chat_id,
                           to_send[1],
                           parse_mode="MARKDOWN",
                           disable_web_page_preview=True,
                       )
                       sleep(randrange(2, 4))
                   except BadRequest as excp:
                       LOGGER.exception("Error in : " + excp.chat)


       update.effective_message.reply_text(
           "Broadcast complete.\nFailed: {} groups.\nSuccess: {} groups.".format(failed, succ)
       )


__mod_name__ = "Broadcast"

__help__ = """
*Broadcast*
(Must be Admin)

*Commands:*
 • /bcast <text> : do a broadcast to the group I'm in.


*Example:*
 • /bcast Sini ada TMO, link >> @LynxUpdates


📝Note :
“Gunakanlah dengan bijak!
 Jika tidak bijak, resiko ditanggung sendiri.”
"""
