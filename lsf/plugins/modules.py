import importlib
import collections

from lsf import dispatcher, lynx_client
from lsf.__help__ import (
    CHAT_SETTINGS,
    DATA_EXPORT,
    DATA_IMPORT,
    HELPABLE,
    IMPORTED,
    MIGRATEABLE,
    STATS,
    USER_INFO,
    USER_SETTINGS
)
from lsf.handlers.valid import dev_plus, sudo_plus
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, run_async


@dev_plus
def load(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)[1]
    load_messasge = message.reply_text(
        f"Attempting to load plugins : <b>{text}</b>", parse_mode=ParseMode.HTML
    )

    try:
        imported_plugins = importlib.import_plugins("lsf.plugins." + text)
    except:
        load_messasge.edit_text("Does that plugins even exist?")
        return

    if not hasattr(imported_plugins, "__mod_name__"):
        imported_plugins.__mod_name__ = imported_plugins.__name__

    if imported_plugins.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_plugins.__mod_name__.lower()] = imported_plugins
    else:
        load_messasge.edit_text("Plugins already loaded.")
        return
    if "__handlers__" in dir(imported_plugins):
        handlers = imported_plugins.__handlers__
        for handler in handlers:
            if not isinstance(handler, tuple):
                dispatcher.add_handler(handler)
            else:
                if isinstance(handler[0], collections.Callable):
                    callback, telethon_event = handler
                    telethn.add_event_handler(callback, telethon_event)
                else:
                    handler_name, priority = handler
                    dispatcher.add_handler(handler_name, priority)
    else:
        IMPORTED.pop(imported_plugins.__mod_name__.lower())
        load_messasge.edit_text("The plugins cannot be loaded.")
        return

    if hasattr(imported_plugins, "__help__") and imported_plugins.__help__:
        HELPABLE[imported_plugins.__mod_name__.lower()] = imported_plugins

    # Chats to migrate on chat_migrated events
    if hasattr(imported_plugins, "__migrate__"):
        MIGRATEABLE.append(imported_plugins)

    if hasattr(imported_plugins, "__stats__"):
        STATS.append(imported_plugins)

    if hasattr(imported_plugins, "__user_info__"):
        USER_INFO.append(imported_plugins)

    if hasattr(imported_plugins, "__import_data__"):
        DATA_IMPORT.append(imported_plugins)

    if hasattr(imported_plugins, "__export_data__"):
        DATA_EXPORT.append(imported_plugins)

    if hasattr(imported_plugins, "__chat_settings__"):
        CHAT_SETTINGS[imported_plugins.__mod_name__.lower()] = imported_plugins

    if hasattr(imported_plugins, "__user_settings__"):
        USER_SETTINGS[imported_plugins.__mod_name__.lower()] = imported_plugins


    load_messasge.edit_text(
        "Successfully loaded plugins : <b>{}</b>".format(text), parse_mode=ParseMode.HTML
    )


@dev_plus
def unload(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)[1]
    unload_messasge = message.reply_text(
        f"Attempting to unload plugins : <b>{text}</b>", parse_mode=ParseMode.HTML
    )

    try:
        imported_plugins = importlib.import_plugins("lsf.plugins." + text)
    except:
        unload_messasge.edit_text("Does that plugins even exist?")
        return

    if not hasattr(imported_plugins, "__mod_name__"):
        imported_plugins.__mod_name__ = imported_plugins.__name__
    if imported_plugins.__mod_name__.lower() in IMPORTED:
        IMPORTED.pop(imported_plugins.__mod_name__.lower())
    else:
        unload_messasge.edit_text("Can't unload something that isn't loaded.")
        return
    if "__handlers__" in dir(imported_module):
        handlers = imported_plugins.__handlers__
        for handler in handlers:
            if isinstance(handler, bool):
                unload_messasge.edit_text("This plugins can't be unloaded!")
                return
            elif not isinstance(handler, tuple):
                dispatcher.remove_handler(handler)
            else:
                if isinstance(handler[0], collections.Callable):
                    callback, telethon_event = handler
                    telethn.remove_event_handler(callback, telethon_event)
                else:
                    handler_name, priority = handler
                    dispatcher.remove_handler(handler_name, priority)
    else:
        unload_messasge.edit_text("The plugins cannot be unloaded.")
        return

    if hasattr(imported_plugins, "__help__") and imported_plugins.__help__:
        HELPABLE.pop(imported_plugins.__mod_name__.lower())

    # Chats to migrate on chat_migrated events
    if hasattr(imported_plugins, "__migrate__"):
        MIGRATEABLE.remove(imported_plugins)

    if hasattr(imported_plugins, "__stats__"):
        STATS.remove(imported_plugins)

    if hasattr(imported_plugins, "__user_info__"):
        USER_INFO.remove(imported_plugins)

    if hasattr(imported_plugins, "__import_data__"):
        DATA_IMPORT.remove(imported_plugins)

    if hasattr(imported_plugins, "__export_data__"):
        DATA_EXPORT.remove(imported_plugins)

    if hasattr(imported_plugins, "__chat_settings__"):
        CHAT_SETTINGS.pop(imported_plugins.__mod_name__.lower())

    if hasattr(imported_plugins, "__user_settings__"):
        USER_SETTINGS.pop(imported_plugins.__mod_name__.lower())

    unload_messasge.edit_text(
        f"Successfully unloaded plugins : <b>{text}</b>", parse_mode=ParseMode.HTML
    )


@sudo_plus
def listplugins(update: Update, context: CallbackContext):
    message = update.effective_message
    plugins_list = []

    for helpable_plugins in HELPABLE:
        helpable_plugins_info = IMPORTED[helpable_plugins]
        file_info = IMPORTED[helpable_plugins_info.__mod_name__.lower()]
        file_name = file_info.__name__.rsplit("lsf.plugins.", 1)[1]
        mod_name = file_info.__mod_name__
        plugins_list.append(f"- <code>{mod_name} ({file_name})</code>\n")
    plugins_list = "Following plugins are loaded : \n\n" + "".join(plugins_list)
    message.reply_text(plugins_list, parse_mode=ParseMode.HTML)


LOAD_HANDLER = CommandHandler("load", load, run_async=True)
UNLOAD_HANDLER = CommandHandler("unload", unload, run_async=True)
LISTPLUGINS_HANDLER = CommandHandler("listplugins", listplugins, run_async=True)

dispatcher.add_handler(LOAD_HANDLER)
dispatcher.add_handler(UNLOAD_HANDLER)
dispatcher.add_handler(LISTPLUGINS_HANDLER)
