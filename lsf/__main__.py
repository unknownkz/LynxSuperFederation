# Copyright © 2022 Unknown (The MIT License)
# All Rights Reserved

import datetime
import os
import platform
import re
import sys
import time
from platform import node, python_version, python_build, python_compiler
from sys import argv

from psutil import boot_time, cpu_percent, disk_usage, virtual_memory
from telegram import Message, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update, __version__
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import escape_markdown, mention_html

from lsf import (
    OWNER_ID,
    OWNER_USERNAME,
    dispatcher,
    StartTime,
    LOGGER,
    SUPPORT_CHAT,
    WEBHOOK,
    CERT_PATH,
    PORT,
    URL,
    TGB_TOKEN,
    SERVER_IP,
    lynx_client,
    updater,
    xx,
)
from lsf.__help__ import (
    get_help,
    help_button,
    get_settings,
    settings_button,
    migrate_chats,
    send_help,
    send_admin_help,
    send_user_help,
    user_help_button,
    send_settings,
    admin_help_button,
    tools_help_button,
    send_tools_help,
    HELP_STRINGS,
    IMPORTED,
    HELPABLE,
    ADMIN,
    USER,
    TOOLS,
)
from lsf.database import users_sql as safe
from lsf.handlers.altaraction import commands_functions
from lsf.handlers.valid import is_user_admin
from lsf.plugins import ALL_PLUGINS


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """ Hi *{}*! My name is *{}*.

A telegram group management bot.
I'm here to help you to manage your groups.
Hit /help for my usage information or click the button bellow.

So what are you waiting for?
*Add me in your groups and give me full rights to make me function well.*


*INFO SERVER*
`Starting from: {}
{} users and {} chats.`
"""

keybo = [
    [
        InlineKeyboardButton(text="Add to Group 👥", url=f"https://t.me/lynxsfrobot?startgroup=true"),
        InlineKeyboardButton(text="Gban Logs 🚫", url="https://t.me/+04O6oVR6cwwwMWU9"),
    ]
]

keybo += [
    [
        InlineKeyboardButton(text="Admins", callback_data="admin_back"),
        InlineKeyboardButton(text="Users", callback_data="user_back"),
        InlineKeyboardButton(text="Tools", callback_data="tools_back"),
    ]
]

keybo += [
    [
        InlineKeyboardButton(text="About ⁉️", callback_data="lynx_"),
    ]
]

keybo += [
    [
        InlineKeyboardButton(text="All Command ›_", callback_data="help_back"),
    ]
]


@commands_functions
def start(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    first_name = update.effective_user.first_name
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup([[InlineKeyboardButton(text="‹_ Back", callback_data="help_back")]]),
                )
                send_admin_help(
                    update.effective_chat.id,
                    ADMIN[mod].__help__,
                    InlineKeyboardMarkup([[InlineKeyboardButton(text="‹_ Back", callback_data="admin_back")]]),
                )
                send_user_help(
                    update.effective_chat.id,
                    USER[mod].__help__,
                    InlineKeyboardMarkup([[InlineKeyboardButton(text="‹_ Back", callback_data="user_back")]]),
                )
                send_tools_help(
                    update.effective_chat.id,
                    USER[mod].__help__,
                    InlineKeyboardMarkup([[InlineKeyboardButton(text="‹_ Back", callback_data="tools_back")]]),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_message.reply_text(
                text=PM_START_TEXT.format(
                    escape_markdown(first_name),
                    escape_markdown(context.bot.first_name),
                    escape_markdown(uptime),
                    safe.num_users(),
                    safe.num_chats(),
                ),
                reply_markup=InlineKeyboardMarkup(keybo),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        mem = virtual_memory()
        cpu = cpu_percent()
        disk = disk_usage("/")
        uname = platform.uname()
        app_time = get_readable_time((time.time() - StartTime))
        uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y/%m/%d %H:%M")
        status = "<b>=======[ L y n x System ]=======</b>\n\n"
        status += "<b>Lynx uptime:</b> <code>" + str(app_time) + "</code\n"
        status += "<b>System uptime:</b> <code>" + str(uptime) + "</code>\n"
        status += "<b>System:</b> <code>" + str(uname.system) + "</code>\n"
        status += "<b>Network name:</b> <code>" + str(node()) + "</code>\n"
        status += "<b>Release:</b> <code>" + str(uname.release) + "</code>\n"
        status += "<b>Version:</b> <code>" + str(uname.version) + "</code>\n"
        status += "<b>Machine:</b> <code>" + str(uname.machine) + "</code>\n"
        status += "<b>Processor:</b> <code>" + str(uname.processor) + "</code>\n\n--------------------"
        status += "<b>CPU usage:</b> <code>" + str(cpu) + " %</code>\n"
        status += "<b>Ram usage:</b> <code>" + str(mem[2]) + " %</code>\n"
        status += "<b>Storage usage:</b> <code>" + str(disk[3]) + " %</code>\n\n--------------------"
        status += "<b>Python version:</b> <code>" + python_version() + "</code>\n"
        status += "<b>Python compiler:</b> <code>" + str(python_compiler()) + "</code>\n"
        status += "<b>Python build:</b> <code>" + str(python_build(buildno, builddate)) + "</code>\n"
        status += "<b>Library version:</b> <code>" + str(__version__) + "</code>\n\n"
        status += "For more usage information,\nplease press /settings or click the button below"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Support", url="https://t.me/LSF_SupportGroup"),
                    InlineKeyboardButton(text="Lynx News", url="https://t.me/LynxUpdates"),
                ],
                [
                    InlineKeyboardButton(text="Donate 💰", url="https://paypal.me/unknownkz"),
                    InlineKeyboardButton(text="Maintainers", url="https://t.me/xelyourslured"),
                ],
                [
                    InlineKeyboardButton(text="All Command ›_", url=f"t.me/lynxsfrobot?start=help"),
                ],
            ]
        )
        message.reply_photo(
            photo="https://ibb.co/TB4F9KZ",
            quote=True or False,
            caption=(status),
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )


PM_START_TEXT2 = """
A Powerful Telegram Group Management Bot
built to help you manage Group easily.

*About me:*
`I was created to manage your groups
on telegram and focuses on the Federation.
I made this to root out telegram users who
global broadcast, nsfw or spam etc.`

*INFO SERVER*
`Starting from: {}
{} users and {} chats.`
"""

keyb = [
    [
        InlineKeyboardButton(text="Add to Group 👥", url=f"https://t.me/lynxsfrobot?startgroup=true"),
        InlineKeyboardButton(text="Lynx News", url="https://t.me/LynxUpdates"),
    ]
]

keyb += [
    [
        InlineKeyboardButton(text="Donate 💰", url="https://paypal.me/unknownkz"),
        InlineKeyboardButton(text="‹_ Back", callback_data="lynx_info_plugins"),
    ]
]


def lynx_about_callback(update: Update, context: CallbackContext):
    first_name = update.effective_user.first_name
    query = update.callback_query
    uptime = get_readable_time((time.time() - StartTime))
    if query.data == "lynx_":
        query.message.edit_text(
            text=PM_START_TEXT2.format(
                escape_markdown(uptime),
                safe.num_users(),
                safe.num_chats(),
            ),
            reply_markup=InlineKeyboardMarkup(keyb),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )
    elif query.data == "lynx_info_plugins":
        query.message.edit_text(
            text=PM_START_TEXT.format(
                escape_markdown(first_name),
                escape_markdown(context.bot.first_name),
                escape_markdown(uptime),
                safe.num_users(),
                safe.num_chats(),
            ),
            reply_markup=InlineKeyboardMarkup(keybo),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )


def main():
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            stronger = "My dear Owner , I'm Working Again. Thanks to make me live."
            dispatcher.bot.sendMessage(f"@{OWNER_ID}", stronger)
        except Unauthorized:
            LOGGER.warning("Lynx isnt able to send message to support_chat, go and check!")
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start, pass_args=True, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*", run_async=True)
    admin_help_callback_handler = CallbackQueryHandler(admin_help_button, pattern=r"admin_.*", run_async=True)
    user_help_callback_handler = CallbackQueryHandler(user_help_button, pattern=r"user_.*", run_async=True)
    tools_help_callback_handler = CallbackQueryHandler(tools_help_button, pattern=r"tools_.*", run_async=True)

    about_callback_handler = CallbackQueryHandler(lynx_about_callback, pattern=r"lynx_", run_async=True)

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_", run_async=True)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats, run_async=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(admin_help_callback_handler)
    dispatcher.add_handler(user_help_callback_handler)
    dispatcher.add_handler(tools_help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen=SERVER_IP, port=PORT, url_path=URL + TGB_TOKEN + "/")

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TGB_TOKEN + "/", certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TGB_TOKEN + "/")

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(
            allowed_updates=Update.ALL_TYPES,
            timeout=15,
            read_latency=4,
            drop_pending_updates=True,
        )

    if len(argv) not in (1, 3, 4):
        lynx_client.disconnect()
    else:
        lynx_client.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded plugins: " + str(ALL_PLUGINS))
    lynx_client.start(bot_token=TGB_TOKEN)
    xx.start()
    main()


try:
    from . import STRING_SESSION, SESSION_STRING, API_ID, API_HASH, TGB_TOKEN
finally:
    del STRING_SESSION
    del SESSION_STRING
    del TGB_TOKEN
    del API_HASH
    del API_ID
