import os
import subprocess
import sys
import lsf

from contextlib import suppress
from time import sleep

from lsf.handlers.valid import dev_plus
from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        state = "Lockdown is " + "on" + "yes" if not lsf.ALLOW_CHATS else "off" + "no"
        update.effective_message.reply_text(f"Current state: {state}")
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


@dev_plus
def gitpull(update: Update, context: CallbackContext):
    lynx_msg = update.effective_message.reply_text(
        "Pulling all changes from remote and then attempting to restart.",
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    lynx_msg_text = lynx_msg.text + "\n\nPulling... "

    for i in reversed(range(5)):
        lynx_msg.edit_text(lynx_msg_text + str(i + 1))
        sleep(1)

    lynx_msg.edit_text("Restarted.")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@dev_plus
def rebooting(update: Update, context: CallbackContext):
    lynx_msg = update.effective_message.reply_text(
        "Restarting... please wait!",
    )
    os.system("restart.bat")
    os.execv("start.bat", sys.argv)
    lynx_msg.edit_text("Done.. I've come back to life")




LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull, run_async=True)
REBOOTING_HANDLER = CommandHandler("rebooting", rebooting, run_async=True)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups, run_async=True)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(REBOOTING_HANDLER)

__mod_name__ = "Controllers"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, REBOOTING_HANDLER, ALLOWGROUPS_HANDLER]
