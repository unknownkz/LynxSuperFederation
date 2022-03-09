# @unknownkz
from random import randrange
from time import sleep

from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from telegram.ext import CallbackContext

from ... import LOGGER
from ...database import users_sql as sql
from ...handlers.valid import is_user_admin
from ...handlers.valid import bot_admin as absolute
from ..commander import Lynxcmd

CHAT_GROUP = 30


@Lynxcmd("bcast", group=CHAT_GROUP)
@absolute
def broadcasts(update: Update, context: CallbackContext):
    wx = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    xx = is_user_admin(chat, user.id)
    if not xx:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Help ❔", url="t.me/lynxsfrobot?start=help"),
                ],
                [
                    InlineKeyboardButton(text="Lynx News", url="https://t.me/LynxUpdates"),
                ],
            ]
        )
        phs = update.effective_message
        phs.reply_photo(
            photo="https://ibb.co/9V51wSC",
            quote=True or False,
            caption="For more information, please click the button below.",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
        sleep(10)
        wx.delete()
        phs.delete()

    sending = wx.text.split(None, 1) | wx.photo.split(None, 1) | wx.sticker.split(None, 1) | wx.audio.split(None, 1)
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

        mesg = update.effective_message
        keyboard1 = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Lynx News", url="https://t.me/LynxUpdates"),
                ],
            ]
        )
        mesg.reply_photo(
            photo="https://ibb.co/vjtp4tW",
            quote=True or False,
            caption="Broadcast complete.\n❎ Failed: {} groups.\n✅ Success: {} groups.".format(failed, succ),
            reply_markup=keyboard1,
            parse_mode=ParseMode.MARKDOWN,
        )
        sleep(10)
        mesg.delete()
        wx.delete()

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
