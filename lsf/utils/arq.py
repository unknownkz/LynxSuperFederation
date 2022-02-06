from aiohttp import ClientSession
from Python_ARQ import ARQ
from .. import ARQ_API_URL, ARQ_API_KEY, aiohttpsession

# Aiohttp Client
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
