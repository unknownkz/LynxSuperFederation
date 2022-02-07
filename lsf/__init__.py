# Copyleft © 2022 Unknown
# Don't Delete this if u kang.
"""
Credit: @Unknownkz | @notudope | @AnimeKaizoku
"""

import logging
import os
import sys
import time
from inspect import getfullargspec
from logging.handlers import RotatingFileHandler
from os import path, remove
from pathlib import Path

import spamwatch
import telegram.ext as tg
from aiohttp import ClientSession
from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from pyrogram.types import Chat, Message
from Python_ARQ import ARQ
from telethon import TelegramClient
from telethon.sessions import MemorySession, StringSession

from .handlers import CustomCommandHandler, CustomMessageHandler, CustomRegexHandler

StartTime = time.time()

if path.exists("logs/lsf.log"):
    remove("logs/lsf.log")

logging.basicConfig(
    format="%(asctime)s || [%(levelname)s] - ℅(name)s - %(message)s",
    level=logging.INFO,
    handlers=[
        RotatingFileHandler("logs/lsf.log", maxBytes=20480, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("asyncio").setlevel(logging.ERROR)
logging.getLogger("Telethon").setlevel(logging.ERROR)
logging.getLogger("telethon.network.mtprotosender").setlevel(logging.ERROR)
LOGGER = logging.getLogger("LFS")

if sys.version_info[0] < 3 or sys.version_info[1] < 10:
    LOGGER.error(
        "You MUST have a python version of at least 3.10! Multiple features depend on this Bot quitting"
    )
    sys.exit(1)

dirs = ["logs", "bin"]
for dir in dirs:
    if not path.exists(dir):
        Path(dir).mkdir(parents=True, exist_ok=True)
    else:
        for file in Path(path.realpath(dir)).rglob("*.*"):
            if path.isfile(file):
                remove(file)

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
        raise Exception(
            "Your SUDO or DEV Users list does not contain valid integers")

    try:
        SUPPORT_ID = {int(x) for x in os.environ.get("SUPPORT_ID", "").split()}
    except ValueError:
        raise Exception(
            "Your SUPPORT Users list does not contain valid integers")

    try:
        WHITELIST_ID = {int(x)
                        for x in os.environ.get("WHITELIST_ID", "").split()}
    except ValueError:
        raise Exception(
            "Your WHITELISTED Users list does not contain valid integers")

    try:
        TIGERS_ID = {int(x) for x in os.environ.get("TIGERS_ID", "").split()}
    except ValueError:
        raise Exception(
            "Your TIGER Users list does not contain valid integers")

    TGB_USERNAME = os.environ.get("TGB_USERNAME")
    EVENT_LOGS = os.environ.get("EVENT_LOGS")
    ERROR_LOGS = os.environ.get("ERROR_LOGS")
    STRING_SESSION = os.environ.get("STRING_SESSION")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
    ARQ_API = os.environ.get("ARQ_API")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")

    WORKERS = int(os.environ.get("WORKERS", 8))
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API")
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "lsf_supportgroup")
    TGB_ID = int(os.environ.get("TGB_ID"))
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = ARQ_API
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", True))
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")

    try:
        BLACKLIST_CHAT = set(
            int(x) for x in os.environ.get("BLACKLIST_CHAT", "").split()
        )
    except ValueError:
        raise Exception(
            "Your BLACKLISTED Chats list does'nt contain valid integers.")

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
        raise Exception(
            "Your SUDO or DEV Users list does not contain valid integers")

    try:
        SUPPORT_ID = {int(x) for x in Unknown.SUPPORT_ID or []}
    except ValueError:
        raise Exception(
            "Your SUPPORT Users list does not contain valid integers")

    try:
        WHITELIST_ID = {int(x) for x in Unknown.WHITELIST_ID or []}
    except ValueError:
        raise Exception(
            "Your WHITELISTED Users list does not contain valid integers")

    try:
        TIGERS_ID = {int(x) for x in Unknown.TIGERS_ID or []}
    except ValueError:
        raise Exception(
            "Your TIGER Users list does not contain valid integers")

    EVENT_LOGS = Unknown.EVENT_LOGS
    ERROR_LOGS = Unknown.ERROR_LOGS
    WEBHOOK = Unknown.WEBHOOK
    URL = Unknown.URL
    PORT = Unknown.PORT
    CERT_PATH = Unknown.CERT_PATH
    API_ID = Unknown.API_ID
    API_HASH = Unknown.API_Unknown
    DB_URI = Unknown.SQLALCHEMY_DATABASE_URI
    MONGO_DB_URI = Unknown.MONGO_DB_URI
    ARQ_API = Unknown.ARQ_API_KEY
    ARQ_API_URL = Unknown.ARQ_API_URL
    LOAD = Unknown.LOAD
    TEMP_DOWNLOAD_DIRECTORY = Unknown.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Unknown.OPENWEATHERMAP_ID
    NO_LOAD = Unknown.NO_LOAD
    HEROKU_API_KEY = Unknown.HEROKU_API_KEY
    HEROKU_APP_NAME = Unknown.HEROKU_APP_NAME
    DEL_CMDS = Unknown.DEL_CMDS
    STRICT_GBAN = Unknown.STRICT_GBAN
    WORKERS = Unknown.WORKERS
    BAN_STICKER = Unknown.BAN_STICKER
    ALLOW_EXCL = Unknown.ALLOW_EXCL
    SUPPORT_CHAT = Unknown.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Unknown.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Unknown.SPAMWATCH_API
    INFOPIC = Unknown.INFOPIC
    TGB_USERNAME = Unknown.TGB_USERNAME
    STRING_SESSION = Unknown.STRING_SESSION

    try:
        BLACKLIST_CHAT = {int(x) for x in Unknown.BLACKLIST_CHAT or []}
    except ValueError:
        raise Exception(
            "Your BLACKLISTED Chats list does not contain valid integers")

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
print("[INFO]: INITIALIZING AIOHTTP SESSION")
aiohttpsession = ClientSession()

print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

lynx_tgb = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

try:
    lynx_tgb.start()
except BaseException:
    print("Lynx Error ! Have you added a STRING_SESSION in Deploying?")
    sys.exit(1)

fed_lynx = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TGB_TOKEN,
    workers=min(32, os.cpu_count() + 8),
)
apps = []
apps.append(fed_lynx)


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):

        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id

        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:

                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


CHANNELS = {}
SD_ID = list(SD_ID) + list(DEV_ID)
DEV_ID = list(DEV_ID)
WHITELIST_ID = list(WHITELIST_ID)
SUPPORT_ID = list(SUPPORT_ID)
TIGERS_ID = list(TIGERS_ID)


tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
