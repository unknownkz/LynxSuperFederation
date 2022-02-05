import json
import sys
import aiohttp
from time import time
from random import randint
from aiohttp import ClientSession
from google_trans_new import google_translator
from Python_ARQ import ARQ
from search_engine_parser import GoogleSearch
from lsf import ARQ_API_URL, ARQ_API_KEY, aiohttpsession

# Aiohttp Client
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
