# @unknownkz
from random import randrange
from time import sleep

from telegram import Update, ParseMode
from telegram.error import BadRequest, TelegramError, ChatMigrated
from telegram.ext import CallbackContext, Filters, CommandHandler

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
        wx.reply_text("Only admin can do live broadcast.")
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
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
                sleep(randrange(2, 4))
                succ += 1
            except (ChatMigrated, BadRequest) as excp:
                escp = get_exception(excp)
                if escp == "An unknown error occurred":
                    try:
                        context.bot.sendMessage(
                            int(xz.chat_id),
                            sending[1],
                            parse_mode=ParseMode.MARKDOWN,
                            disable_web_page_preview=True,
                        )
                        sleep(randrange(2, 4))
                    except TelegramError:
                        failed += 1
                        LOGGER.warning(
                            "Couldn't send broadcast to %s, group name %s",
                            str(xz.chat_id),
                            str(xz.chat_name),
                        )

        update.effective_message.reply_photo(
            photo="https://ibb.co/vjtp4tW",
            caption="Broadcast complete.\n❎ Failed: {} groups.\n✅ Success: {} groups.".format(failed, succ),
            parse_mode=ParseMode.HTML,
            disable_web_page_priview=False,
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
