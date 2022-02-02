import json
import os

def get_user_list(config, key):
    with open("{}/lsf/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]

class Config(object):
    """Configs to setup LSF"""
    LOGGER = True
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    OWNER_ID = os.environ.get("OWNER_ID")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME")
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT")
    JOIN_LOGGER = int(os.environ.get("JOIN_LOGGER"))
    EVENT_LOGS = int(os.environ.get("EVENT_LOGS"))
    CASH_API_KEY = os.environ.get("CASH_API_KEY")
    TIME_API_KEY = os.environ.get("TIME_API_KEY")
    WALL_API = os.environ.get("WALL_API")
    WORKERS = int(os.environ.get("WORKERS")) or os.cpu_count() + 8
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    # OPTIONAL ID
    SD_ID = get_user_list("user_creation_list.json", "sudos")
    DEV_ID = get_user_list("user_creation_list.json", "devs")
    SUPPORT_ID = get_user_list("user_creation_list.json", "supports")
    TIGERS_ID = get_user_list("user_creation_list.json", "tigers")
    WHITELIST_ID = get_user_list("user_creation_list.json", "whitelists")

    DONATION_LINK = None
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True
    STRICT_GBAN = True
    BAN_STICKER = None
    ALLOW_EXCL = True
    AI_API_KEY = None
    BL_CHATS = []
    SPAMMERS = None
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
