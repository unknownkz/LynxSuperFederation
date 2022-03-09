import html
import json
import os
import re
import requests
from time import sleep
from telegram import (
    ParseMode,
    CallbackQuery,
    Chat,
    MessageEntity,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
    Bot,
    User,
)
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    DispatcherHandlerStop,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown

from lsf import dispatcher, updater, SUPPORT_CHAT
from lsf.database import auto_chatbot_sql as sql
from lsf.handlers.valid import user_admin, user_admin_no_reply, dev_plus
from lsf.utils.customfilters import CustomFilters

from .log_channel import gloggable


@user_admin_no_reply
@gloggable
def lynxrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_lynx = sql.rem_lynx(chat.id)
        if is_lynx:
            is_lynx = sql.rem_lynx(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI DISABLED ❌\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Lynx Chat-Bot disable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin_no_reply
@gloggable
def lynxadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_lynx = sql.set_lynx(chat.id)
        if is_lynx:
            is_lynx = sql.set_lynx(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI ENABLE ✅\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Lynx Chat-Bot Enable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin
@gloggable
def lynx(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message
    msg = "Choose an option"
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Enable", callback_data="add_chat({})")],
            [InlineKeyboardButton(text="Disable", callback_data="rm_chat({})")],
        ]
    )
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def lynx_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "lynx":
        return True
    if reply_message:
        if reply_message.from_user.id == context.bot.get_me().id:
            return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_lynx = sql.is_lynx(chat_id)
    if not is_lynx:
        return

    if message.text and not message.document:
        if not lynx_message(context, message):
            return
        Message = message.text
        bot.send_chat_action(chat_id, action="typing")
        lynxurl = requests.get(
            "https://www.kukiapi.xyz/api/apikey=KUKIg76Fg4EIo/Natsunagi/@xelyourslurred/message=" + Message
        )
        Lynx = json.loads(lynxurl.text)
        lynx = Lynx["reply"]
        sleep(0.3)
        message.reply_text(lynx, timeout=60)


@dev_plus
def listchatbot(update: Update, context: CallbackContext):
    chats = sql.get_all_lynx_chats()
    text = "<b>Lynx-Bot Enabled Chats</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title or x.first_name
            text += f"• <code>{name}</code>\n"
        except (BadRequest, Unauthorized):
            sql.rem_lynx(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


__help__ = """
Chatbot utilizes from Kuki's api which allows Kuki to talk and provide a more interactive group chat experience.

*Admins only Commands*:
 • /chatbot : Shows chatbot control panel
  
Powered by *ItelAI* ( @KukiUpdates )
"""

__mod_name__ = "ChatBot"


CHATBOTK_HANDLER = CommandHandler("chatbot", lynx, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(lynxadd, pattern=r"add_chat", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(lynxrm, pattern=r"rm_chat", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
    run_async=True,
)
LIST_ALL_CHATS_HANDLER = CommandHandler("listchatbot", listchatbot, filters=CustomFilters.dev_filter, run_async=True)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(LIST_ALL_CHATS_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    LIST_ALL_CHATS_HANDLER,
    CHATBOT_HANDLER,
]
