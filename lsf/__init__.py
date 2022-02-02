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

if path.exist("logs/lsf.log"):
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
logging.getLogger("asyncio")setlevel(logging.ERROR)
logging.getLogger("Telethon")setlevel(logging.ERROR)
logging.getLogger("telethon.network.mtprotosender")setlevel(logging.ERROR)
LOGGER = logging.getLogger("LFS")
