# @unknownkz
from random import randrange
from time import sleep

from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.error import TelegramError
from telegram.ext import CallbackContext

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

# def key_build(*args, **kwargs, chat=None) -> List:
#    if not chat:
#        buttons = (
#            [
#                EqInlineKeyboardButton(
#                    bcast,
#                    callback_data="verify_ads",
#                )
#            ]
#        )
#    else:
#        buttons = (
#            [
#                EqInlineKeyboardButton(
#                    bcast
#                    callback_data="verify_ads",
#                )
#            ]
#        )


def verify_ads(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(keyboard1)
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text="Click the button below if you want to use the broadcast feature.",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False,
        reply_markup=keyboard1,
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
                text="✅Succesfully\nNow send message to broadcast.",
                reply_markup=ReplyKeyboardRemove(),
                tparse_mode=ParseMode.MARKDOWN,
                timeout=30,
            )
            return

    elif query.data == "verify_cancel":
        hxz = update.effective_message
        msg = hxz.reply_text(
            text="Broadcast cancelled.",
            reply_markup=ReplyKeyboardRemove(),
        )
        sleep(4)
        msg.delete()


@Lynxcmd("bcast", group=CHAT_GROUP)
@absolute
def broadcasts(update: Update, context: CallbackContext):
    wx = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    contol = context.args
    xx = is_user_admin(chat, user.id)
    if len(contol) >= 1:
        if contol[0].lower() == "bcast":
            verify_ads(update.effective_chat.id)
            return

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
