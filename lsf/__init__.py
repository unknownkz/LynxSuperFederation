import os
import sys
import json
import time
import asyncio
import logging
import spamwatch
import telegram.ext as tg

from pathlib import Path
from inspect import getfullargspec
from aiohttp import ClientSession
from Python_ARQ import ARQ
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.sessions import MemorySession
from pyrogram.types import Message
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Chat, User
from logging.handlers import RotatingFileHandler

StartTime = time.time()

if path.exists("logs/lsf.log"):
    remove("logs/lsf.log")

logging.basicConfig(
    format="%(asctime)s || [%(levelname)s] - ℅(name)s - %(message)s",
    level=logging.INFO,
    handlers=[
        RotatingFileHandler(
             "logs/lsf.log", maxBytes=20480, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("asyncio").setlevel(logging.ERROR)
logging.getLogger("Telethon").setlevel(logging.ERROR)
logging.getLogger("telethon.network.mtprotosender").setlevel(logging.ERROR)
LOGGER = logging.getLogger("LFS")

if sys.version_info[0] < 3 or sys.version_info[1] < 10:
    LOGGER.error("You MUST have a python version of at least 3.10! Multiple features depend on this Bot quitting")
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
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer, please check again.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

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

    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    ERROR_LOGS = os.environ.get("ERROR_LOGS", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    ARQ_API = os.environ.get("ARQ_API", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    WORKERS = int(os.environ.get("WORKERS", 24))
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
    BOT_ID = int(os.environ.get("BOT_ID", None))
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = ARQ_API
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    DATABASE_URL = DATABASE_URL.replace(
        "postgres", "postgresql"
    )

    try:
        BLACKLIST_CHAT = set(int(x) for x in os.environ.get("BLACKLIST_CHAT", "").split())
    except ValueError:
        raise Exception("Your BLACKLISTED Chats list does'nt contain valid integers.")
