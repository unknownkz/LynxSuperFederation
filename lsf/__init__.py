# Copyleft © 2022 Unknown
# Don't Delete this if u kang.
"""
Credit: @Unknownkz | @notudope | @AnimeKaizoku
"""

import logging
import sys
import time
from inspect import getfullargspec
from os import path, remove, cpu_count
from os import environ as then
from pathlib import Path
from zoneinfo import ZoneInfo

import heroku3
import spamwatch
from aiohttp import ClientSession
from pyrogram import Client
from Python_ARQ import ARQ
from telegram.ext import Defaults, Updater
from telethon import TelegramClient
from telethon.sessions import MemorySession

StartTime = time.time()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - ℅(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

if not sys.platform.startswith("linux") and not sys.build_platform.startswith("64"):
    LOGGER.error("You have to use linux system first. Such as {} ! quitting..").format(platform())
    sys.exit(1)

if sys.version_info.major < 3 or sys.version_info.minor < 10 or sys.version_info.micro < 2:
    LOGGER.error("You have to use python version of at least {}.{}.{} ! quitting..").format(
        sys.version_info.major(), sys.version_info.minor(), sys.version_info.micro()
    )
    sys.exit(1)

ENV = bool(then.get("ENV", False))

if ENV:
    TGB_TOKEN = then.get("TGB_TOKEN")

    try:
        OWNER_ID = int(then.get("OWNER_ID"))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer, please check again.")

    JOIN_LOGGER = then.get("JOIN_LOGGER")
    OWNER_USERNAME = then.get("OWNER_USERNAME")

    try:
        SD_ID = {int(x) for x in then.get("SD_ID", "").split()}
        DEV_ID = {int(x) for x in then.get("DEV_ID", "").split()}
    except ValueError:
        raise Exception("Your SUDO or DEV Users list does not contain valid integers")

    try:
        SUPPORT_ID = {int(x) for x in then.get("SUPPORT_ID", "").split()}
    except ValueError:
        raise Exception("Your SUPPORT Users list does not contain valid integers")

    try:
        WHITELIST_ID = {int(x) for x in then.get("WHITELIST_ID", "").split()}
    except ValueError:
        raise Exception("Your WHITELISTED Users list does not contain valid integers")

    try:
        TIGERS_ID = {int(x) for x in then.get("TIGERS_ID", "").split()}
    except ValueError:
        raise Exception("Your TIGER Users list does not contain valid integers")

    INFOPIC = bool(then.get("INFOPIC"))
    TGB_USERNAME = then.get("TGB_USERNAME")
    EVENT_LOGS = then.get("EVENT_LOGS")
    ERROR_LOGS = then.get("ERROR_LOGS")
    WEBHOOK = bool(then.get("WEBHOOK"))
    URL = then.get("URL", "")  # Does not contain token
    PORT = int(then.get("PORT", 5000))
    SERVER_IP = then.get("SERVER_IP")
    CERT_PATH = then.get("CERT_PATH")
    API_ID = then.get("API_ID")
    API_HASH = then.get("API_HASH")
    SESSION_STRING = then.get("SESSION_STRING")
    STRING_SESSION = then.get("STRING_SESSION")
    DATABASE_URL = then.get("DATABASE_URL")
    ARQ_API_URL = then.get("ARQ_API_URL")
    ARQ_API_KEY = then.get("ARQ_API_KEY")
    DONATION_LINK = then.get("DONATION_LINK", "paypal.me/unknownkz")
    LOAD = then.get("LOAD", "").split()
    HEROKU_API_KEY = then.get("HEROKU_API_KEY")
    HEROKU_APP_NAME = then.get("HEROKU_APP_NAME")
    TEMP_DOWNLOAD_DIRECTORY = then.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    DEL_CMDS = bool(then.get("DEL_CMDS", False))
    STRICT_GBAN = bool(then.get("STRICT_GBAN", True))
    WORKERS = int(then.get("WORKERS", 8))
    BAN_STICKER = then.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = then.get("ALLOW_EXCL", True)
    ALLOW_CHATS = then.get("ALLOW_CHATS", True)
    SUPPORT_CHAT = then.get("SUPPORT_CHAT")
    SPAMWATCH_SUPPORT_CHAT = then.get("SPAMWATCH_SUPPORT_CHAT")
    SPAMWATCH_API = then.get("SPAMWATCH_API")
    UPSTREAM_REPO_URL = then.get("UPSTREAM_REPO")
    WELCOME_DELAY_KICK_SEC = then.get("WELCOME_DELAY_KICL_SEC")
    TGB_ID = int(then.get("TGB_ID"))
    LOAD = then.get("LOAD", "").split()
    NO_LOAD = then.get("NO_LOAD", "").split()

    try:
        BLACKLIST_CHAT = set(int(x) for x in then.get("BLACKLIST_CHAT", "").split())
    except ValueError:
        raise Exception("Your BLACKLISTED Chats list does'nt contain valid integers.")

else:
    from lsf.config import Development as Unknown

    try:
        OWNER_ID = int(Unknown.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer")

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
    SERVER_IP = Unknown.SERVER_IP
    CERT_PATH = Unknown.CERT_PATH
    API_ID = Unknown.API_ID
    API_HASH = Unknown.API_HASH
    ARQ_API_KEY = Unknown.ARQ_API_KEY
    ARQ_API_URL = Unknown.ARQ_API_URL
    WELCOME_DELAY_KICK_SEC = Unknown.WELCOME_DELAY_KICK_SEC
    UPSTREAM_REPO_URL = Unknown.UPSTREAM_REPO
    DATABASE_URL = Unknown.DATABASE_URL
    DONATION_LINK = Unknown.DONATION_LINK
    LOAD = Unknown.LOAD
    TEMP_DOWNLOAD_DIRECTORY = Unknown.TEMP_DOWNLOAD_DIRECTORY
    NO_LOAD = Unknown.NO_LOAD
    HEROKU_API_KEY = Unknown.HEROKU_API_KEY
    HEROKU_APP_NAME = Unknown.HEROKU_APP_NAME
    DEL_CMDS = Unknown.DEL_CMDS
    STRICT_GBAN = Unknown.STRICT_GBAN
    WORKERS = Unknown.WORKERS
    BAN_STICKER = Unknown.BAN_STICKER
    ALLOW_EXCL = Unknown.ALLOW_EXCL
    ALLOW_CHATS = Unknown.ALLOW_CHATS
    SUPPORT_CHAT = Unknown.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Unknown.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Unknown.SPAMWATCH_API
    SESSION_STRING = Unknown.SESSION_STRING
    INFOPIC = Unknown.INFOPIC
    TGB_USERNAME = Unknown.TGB_USERNAME
    TGB_ID = Unknown.TGB_ID
    TGB_TOKEN = Unknown.TGB_TOKEN
    STRING_SESSION = Unknown.STRING_SESSION
    JOIN_LOGGER = Unknown.JOIN_LOGGER
    OWNER_USERNAME = Unknown.OWNER_USERNAME

    try:
        BLACKLIST_CHAT = {int(x) for x in Unknown.BLACKLIST_CHAT or []}
    except ValueError:
        raise Exception("Your BLACKLISTED Chats list does not contain valid integers")

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except Exception:
        sw = None
        LOGGER.warning("Can't connect to SpamWatch!")

defaults = Defaults(run_async=True)
updater = Updater(TGB_TOKEN, workers=WORKERS, use_context=True)
lynx_client = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher

aiohttpsession = ClientSession()
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

TimeZone = ZoneInfo("Asia/Jakarta")

xx = Client(
    SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TGB_TOKEN,
    workers=min(64, cpu_count() + 16),
)

SD_ID.add(OWNER_ID)
DEV_ID.add(OWNER_ID)

CHANNELS = {}

WHITELIST_ID = list(WHITELIST_ID)
SUPPORT_ID = list(SUPPORT_ID)
TIGERS_ID = list(TIGERS_ID)
