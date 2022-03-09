# @unknownkz
from random import randrange
from time import sleep

from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.error import TelegramError
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

from ... import LOGGER, dispatcher
from ...database import users_sql as sql
from ...handlers.misc import EqInlineKeyboardButton
from ...handlers.valid import is_user_admin
from ...handlers.valid import bot_admin as absolute
from ..commander import Lynxcmd

CHAT_GROUP = 30


keyboard1 = [
    [
        InlineKeyboardButton(text="Verify Now", callback_data="verify_admin"),
        InlineKeyboardButton(text="Cancel", callback_data="verify_cancel"),
    ]
]

"""def key_build(*args, **kwargs, chat=None) -> List:
    if not chat:
         buttons = (
            [
                EqInlineKeyboardButton(
                    bcast,
                    callback_data="verify_ads",
                )
            ]
        )
    else:
        buttons = (
            [
                EqInlineKeyboardButton(
                    bcast
                    callback_data="verify_ads",
                )
            ]
        )
"""

VERIFY_TEXT = "Click the button below if you want to use the broadcast feature."


def verify_ads(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(keyboard1)
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False,
        reply_markup=keyboard,
    )


def verify_admins_call(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    query = update.callback_query
    if query.data == "verify_admin":
        xx = is_user_admin(chat, user.id)
        if not xx:
            update.effective_message.reply_text(
                text="Sorry, u're not admin.",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode=ParseMode.MARKDOWN,
                timeout=30,
            )
        else:
            update.effective_message.reply_text(
                text="✅Succesfully\nNow send message to broadcast.\n/bcadmin <text>",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode=ParseMode.MARKDOWN,
                timeout=30,
            )

    elif query.data == "verify_cancel":
        hxz = update.effective_message
        msg = hxz.reply_text(
            text="Broadcast cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )
        sleep(4)
        msg.delete()

    args = context.args
    if len(args) >= 2:
        to_group = False
    if args[0].lower() == "bcadmin":
        to_group = True
    else:
        to_group = True
        return

    sending = msg.text.split(None, 1)
    if len(sending) >= 2:
        chats = sql.get_all_chats() or []
        succ = failed = 0

    if to_group:
        for xz in chats:
            try:
                context.bot.sendMessage(
                    int(xz.chat_id),
                    sending[1],
                )
                sleep(randrange(2, 4))
                succ += 1
            except TelegramError:
                failed += 1
                LOGGER.warning(
                    "Couldn't send broadcast to %s, group name %s",
                    str(xz.chat_id),
                    str(xz.chat_name),
                )

        msg.reply_photo(
            photo="https://ibb.co/vjtp4tW",
            quote=True or False,
            caption="Broadcast complete.\n❎ Failed: {} groups.\n✅ Success: {} groups.".format(failed, succ),
            parse_mode=ParseMode.HTML,
        )
        sleep(4)
        msg.delete()


@Lynxcmd("bcast")
@absolute
def broadcasts(update: Update, context: CallbackContext):
    wx = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    verify_ads(update.effective_chat.id, VERIFY_TEXT)

    """
    sending = wx.text.split(None, 1)
    if len(sending) >= 2:
        chats = sql.get_all_chats() or []
        succ = failed = 0
        for xz in chats:
            try:
                context.bot.sendMessage(
                    int(xz.chat_id),
                    sending[1],
                )
                sleep(randrange(2, 4))
                succ += 1
            except TelegramError:
                failed += 1
                LOGGER.warning(
                    "Couldn't send broadcast to %s, group name %s",
                    str(xz.chat_id),
                    str(xz.chat_name),
                )

        message = update.effective_message
        ujang = message.reply_photo(
            photo="https://ibb.co/vjtp4tW",
            quote=True or False,
            caption="Broadcast complete.\n❎ Failed: {} groups.\n✅ Success: {} groups.".format(failed, succ),
            parse_mode=ParseMode.HTML,
        )
        sleep(4)
        ujang.delete()
    """


bcast_callback_handler = CallbackQueryHandler(verify_admins_call, pattern=r"bcadmin", run_async=True)

dispatcher.add_handler(bcast_callback_handler)

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
