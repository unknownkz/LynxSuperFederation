# @unknownkz
from random import randrange
from time import sleep
from telegram import Chat, ChatMember, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
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
def broadcasts(user_id: int, member: ChatMember, chat: Chat, update: Update, context: CallbackContext):
    member = chat.get_member(user_id)
    active = member.status in ("administrator", "creator")
    txt = update.effective_message.text
    sending = txt.split(None, 1)
    sent_to_group = True if sending[2] == active
    if not active:
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
        phs = update.effective_message.reply_photo(
            photo="https://ibb.co/9V51wSC",
            quote=True or False,
            caption="For more information, please click the button below.",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
        sleep(15)
        phs.delete()

    chats = sql.get_all_chats() or []
    succ = failed = 0
    if sent_to_group:
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

        keyboard1 = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Lynx News", url="https://t.me/LynxUpdates"),
                ],
            ]
        )
        msg = update.effective_message.reply_photo(
            photo="https://ibb.co/vjtp4tW",
            quote=True or False,
            caption="Broadcast complete.\n❎ Failed: {} groups.\n✅ Success: {} groups.".format(failed, succ),
            reply_markup=keyboard1,
            parse_mode=ParseMode.MARKDOWN,
        )
        sleep(20)
        msg.delete()


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
