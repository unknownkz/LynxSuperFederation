import lsf

from contextlib import suppress

from lsf import dispatcher, ALLOW_CHATS
from lsf.handlers.valid import dev_plus
from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        state = "Lockdown is " + "on" + "yes" if not lsf.ALLOW_CHATS else "off" + "no"
        update.effective_message.reply_text("Current state: {}".format(state())
        return
    if args[0].lower() in ["off", "no"]:
        lsf.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        lsf.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("Format: /lockdown yes/no or off/on")
        return
    update.effective_message.reply_text("Done.. !!!")


@dev_plus
def leave(update: Update, context: CallbackContext):
    hes = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            hes.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "I could'nt leave that group.",
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("I Left Group Chat.")
    else:
        update.effective_message.reply_text("Send a valid chat ID")


LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups, run_async=True)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)

__mod_name__ = "Controllers"
__handlers__ = [LEAVE_HANDLER, ALLOWGROUPS_HANDLER]
