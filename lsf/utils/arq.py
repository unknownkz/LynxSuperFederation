import json
import sys
import aiohttp
from random import randint
from time import time
from aiohttp import ClientSession
from google_trans_new import google_translator
from Python_ARQ import ARQ
from search_engine_parser import GoogleSearch
from lsf import BOT_ID, OWNER_ID, ARQ_API_URL, ARQ_API_KEY, aiohttpsession, fed_lynxbot

# Aiohttp Client
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
