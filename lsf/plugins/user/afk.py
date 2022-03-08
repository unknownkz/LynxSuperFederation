import html
import random
from datetime import datetime
from time import sleep

import humanize
from telegram import MessageEntity, Update, ParseMode
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters

from ... import dispatcher
from ...database import disable_sql
from ...database import afk_sql as sql
from ..commander import Lynxcmd, Lynxmsg
from ..users import get_user_id

AFK_GROUP = 20
AFK_REPLY_GROUP = 20


@Lynxcmd("afk", pass_args=True)
def afk(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(" ", 1)
    user = update.effective_user.id

    if not user:  # ignore-Channels
        update.effective_message.reply_text("Sorry, please use the main account.")
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\n\nYour afk reason was shortened to 100 characters."
    else:
        reason = ""

    sql.set_afk(update.effective_user.id, reason)
    fname = update.effective_user.first_name
    psn = update.effective_message
    sent_ = psn.reply_text("{} is now away! {}".format(fname, notice))
    sleep(7)
    sent_.delete()


@Lynxmsg(Filters.all & Filters.chat_type.groups, group=AFK_GROUP)
def no_longer_afk(update: Update, context: CallbackContext):
    user = update.effective_user.id
    chat = update.effective_chat.id
    message = update.effective_message

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res and not disable_sql.is_command_disabled(chat.id, "afk"):
        if message.new_chat_members:  # dont say msg
            return

        firstname = update.effective_user.first_name
        try:
            options = [
                "{} is here!",
                "{} is back!",
                "{} is now in the chat!",
                "{} is awake!",
                "{} is back online!",
                "{} is finally here!",
                "Welcome back! {}",
                "Where is {}?\nIn the chat!",
            ]
            chosen_option = random.choice(options)
            alive = update.effective_message.reply_text(chosen_option.format(firstname))
            sleep(12)
            alive.delete()
        except BaseException:
            return


def check_afk(update: Update, context: CallbackContext, user_id: int, fst_name: str, userc_id: int):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)
        if not user:
            return

        if int(userc_id) == int(user_id):
            return

        time = humanize.naturaldelta(datetime.now() - user.time)
        if not user.reason:
            res = "{} is afk.\n\nLast seen {} ago.".format(fst_name, time)
            update.effective_message.reply_text(res)

        else:
            res = "{} is afk.\nReason: <code>{}</code>\n\nLast seen {} ago.".format(
                html.escape(fst_name),
                html.escape(user.reason),
                html.escape(time),
            )
            update.effective_message.reply_text(res, parse_mode=ParseMode.HTML)


@Lynxmsg(Filters.all & Filters.chat_type.groups, group=AFK_REPLY_GROUP)
def reply_afk(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user.id
    userc_id = userc.id
    chat = update.effective_chat
    if chat and disable_sql.is_command_disabled(chat.id, "afk"):
        return

    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION],
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION],
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                user_id = get_user_id(message.text[ent.offset : ent.offset + ent.length])

                if not user_id:
                    return

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = bot.get_chat(user_id)
                except BadRequest:
                    print(f"Error: Could not fetch userid {user_id} for AFK plugins")
                    return

                fst_name = chat.first_name
            else:
                return

            check_afk(update, context, user_id, fst_name, userc_id)


__help__ = """
*Away From Keyboard*

 • /afk <reason> : mark yourself as AFK(away from keyboard).

When marked as AFK, any mentions will be replied to with a message to say you're not available!
"""

__mod_name__ = "AFK"
