import html

from ..disable import DisableAbleCommandHandler
from ... import dispatcher, SD_ID
from ...handlers.extraction import extract_user
from telegram.ext import CallbackContext, run_async, CallbackQueryHandler
from ...database import agreement_sql as sql
from ...handlers.valid import user_admin
from .log_channel import loggable
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.utils.helpers import mention_html
from telegram.error import BadRequest


@loggable
@user_admin
def agree(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!",
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status == "administrator" or member.status == "creator":
        message.reply_text(
            "User is already admin - locks, blocklists, and antiflood already don't apply to them.",
        )
        return ""
    if sql.is_agreed(message.chat_id, user_id):
        message.reply_text(
            f"[{member.user['first_name']}](tg://user?id={member.user['id']}) is already agreed in {chat_title}",
            parse_mode=ParseMode.MARKDOWN,
        )
        return ""
    sql.agree(message.chat_id, user_id)
    message.reply_text(
        f"[{member.user['first_name']}](tg://user?id={member.user['id']}) has been agreed in {chat_title}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood.",
        parse_mode=ParseMode.MARKDOWN,
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#AGREED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@loggable
@user_admin
def disagree(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!",
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status == "administrator" or member.status == "creator":
        message.reply_text("This user is an admin, they can't be un-agreed.")
        return ""
    if not sql.is_agreed(message.chat_id, user_id):
        message.reply_text(f"{member.user['first_name']} isn't agreed yet!")
        return ""
    sql.disagree(message.chat_id, user_id)
    message.reply_text(
        f"{member.user['first_name']} is no longer agreed in {chat_title}.",
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNAGREED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@user_admin
def agreed(update, context):
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    msg = "The following users are agreed.\n"
    agreed_users = sql.list_agreed(message.chat_id)
    for i in agreed_users:
        member = chat.get_member(int(i.user_id))
        msg += f"- `{i.user_id}`: {member.user['first_name']}\n"
    if msg.endswith("agreed.\n"):
        message.reply_text(f"No users are agreed in {chat_title}.")
        return ""
    else:
        message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


@user_admin
def agreecheck(update, context):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    user_id = extract_user(message, args)
    member = chat.get_member(int(user_id))
    if not user_id:
        message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!",
        )
        return ""
    if sql.is_agreed(message.chat_id, user_id):
        message.reply_text(
            f"{member.user['first_name']} is an agreed user. Locks, antiflood, and blocklists won't apply to them.",
        )
    else:
        message.reply_text(
            f"{member.user['first_name']} is not an agreed user. They are affected by normal commands.",
        )



def unagreeall(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in SD_ID:
        update.effective_message.reply_text(
            "Only the chat owner can un-agree all users at once.",
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Un-Agree all users", callback_data="unagreeall_user",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Cancel", callback_data="unagreeall_cancel",
                    ),
                ],
            ],
        )
        update.effective_message.reply_text(
            f"Are you sure you would like to un-agree ALL users in {chat.title}? This action cannot be undone.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )



def unagreeall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "unagreeall_user":
        if member.status == "creator" or query.from_user.id in SD_ID:
            agreed_users = sql.list_agreed(chat.id)
            users = [int(i.user_id) for i in agreed_users]
            for user_id in users:
                sql.disagree(chat.id, user_id)
            message.edit_text("Successfully Un-Agree all user in this Chat.")
            return

        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")

        if member.status == "member":
            query.answer("You need to be admin to do this.")
    elif query.data == "unagreeall_cancel":
        if member.status == "creator" or query.from_user.id in SD_ID:
            message.edit_text("Removing of all agreed users has been cancelled.")
            return ""
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")
        if member.status == "member":
            query.answer("You need to be admin to do this.")


__help__ = """
Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.
That's what agreedals are for - agree of trustworthy users to allow them to send

*Admin commands:*
• /agreecheck : Check a user's agree status in this chat.
• /agree : Agree of a user. Locks, blacklists, and antiflood won't apply to them anymore.
• /unagree : Un-agree of a user. They will now be subject to locks, blacklists, and antiflood again.
• /agreed : List all agreed users.
• /unagreeall : Un-agree *ALL* users in a chat. This cannot be undone.
"""

AGREE = DisableAbleCommandHandler("agree", agree, run_async=True)
DISAGREE = DisableAbleCommandHandler("unagree", disagree, run_async=True)
AGREED = DisableAbleCommandHandler("agreed", agreed, run_async=True)
AGREE_CHECK = DisableAbleCommandHandler("agreecheck", agreecheck, run_async=True)
UNAPPROVEALL = DisableAbleCommandHandler("unagreeall", unagreeall, run_async=True)
UNAPPROVEALL_BTN = CallbackQueryHandler(unagreeall_btn, pattern=r"unagreeall_.*", run_async=True)

dispatcher.add_handler(AGREE)
dispatcher.add_handler(DISAGREE)
dispatcher.add_handler(AGREED)
dispatcher.add_handler(AGREE_CHECK)
dispatcher.add_handler(UNAGREEALL)
dispatcher.add_handler(UNAGREEALL_BTN)

__mod_name__ = "Agreement"
__command_list__ = ["agree", "unagree", "agreed", "agreecheck"]
__handlers__ = [AGREE, DISAGREE, AGREED, AGREE_CHECK]
