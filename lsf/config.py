# Create a new config.py or rename this to config.py
# file in same dir and import, then extend this class.
import json
from os import getcwd


def get_user_list(config, key):
    with open("{}/lsf/{}".format(getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Unknown(object):
    LOGGER = True
    # Required
    API_ID = 123456  # integer value, dont use ""
    API_HASH = ""
    TGB_ID = "" # ID ur bot, Go to BotFather and see Token Bot. 6362626
    TGB_TOKEN = "TGB_TOKEN"  # This var used to be BOT TOKEN, adjust accordingly.
    TGB_USERNAME = "LynxSFRobot" # Username Bot, don't use @
    SESSION_STRING = "" # PyrogramSession
    STRING_SESSION = "" # TelethonSession
    OWNER_USERNAME = "xelyourslurred" # ur Username

    # Required ID
    OWNER_ID = 1448477501  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    DEV_ID = 1448477501, 1345272778 # ur id or another id, some like sudo but this is dev
    TIGERS_ID = 137282738, 73727266
    WHITELIST_ID = 208373728, 25262636
    SUPPORT_ID = 182737822, 16263633
    SD_ID = 12337277, 1616262734

    # Log Chat
    SUPPORT_CHAT = "LSF_SupportGroup"  # Your own group for support, do not add the @
    JOIN_LOGGER = (
        -1001756059757
    )  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = (
        -1001756059757
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    ERROR_LOGS = (
        -1001756059757
    )  # Prints any new group the bot is added to, prints just the name and ID.


    # ARQ
    ARQ_API_KEY = "" # Go to @ARQRobot or https://t.me/ARQRobot and /get_key
    ARQ_API_URL = "http://thearq.tech/" # See @ARQUpdates

    # Repository
    UPSTREAM_REPO = "LynxSuperFederation" # Don't change

    # Heroku
    HEROKU_APP_NAME = ""
    HEROKU_API_KEY = ""

    # Recommended
    DATABASE_URL = "postgresql://username:password@localhost:5432/database"  # needed for any database modules # its "URI" and not "URL" as herok and similar ones only accept it as such
    LOAD = []
    NO_LOAD = []
    WEBHOOK = False
    URL = "https://api.telegram.org/bot"
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    DONATION_LINK = "paypal.me/unknownkz"

    # List of Path
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    SERVER_IP = "" # Local host (0.0.0.0)
    WORKERS = (
        16  # Number of subthreads to use. Set as number of threads your processor uses
    )

    INFOPIC = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    BAN_STICKER = ""  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    ALLOW_CHATS = True
    BLACKLIST_CHAT = []  # List of groups that you want blacklisted.
    WELCOME_DELAY_KICK_SEC = "120" # Welcome Delay Kick Seconds


class Production(Unknown):
    LOGGER = True


class Development(Unknown):
    LOGGER = True
