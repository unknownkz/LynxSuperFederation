from ..handlers.valid import dev_plus
from contextlib import suppress
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import TelegramError, Unauthorized
from .commander import Lynxcmd


@Lynxcmd("exit", pass_args=True)
@dev_plus
def exit(update: Update, context: CallbackContext):
    bot = context.bot
    sync = context.args
    if sync:
        chat_id = str(sync[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "Sorry I can't exit this group.",
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("it worked, I've been out in that group.")
    else:
        update.effective_message.reply_text("Please send chat id.")


__mod_name__ = "Exit"
