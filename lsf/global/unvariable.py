# Copyright © 2022 Unknown
# All Rights Reserved

import threading

# Logs
CHANNELS = {}

# Chats
CHAT_BLACKLISTS = {}
CHAT_FLOOD = {}
CHAT_FILTERS = {}
DISABLED = {}

# Global Banned
GBANNED_USERS_LOCK = threading.RLock()
GBAN_SETTING_LOCK = threading.RLock()
GBANNED_LIST = set()
GBANSTAT_LIST = set()

# Blcklisted
BLACKLIST_LOCK = threading.RLock()
BLACKLIST_USERS = set()

# AFK
AFK_USERS = {}

# Filters
CUST_FILT_LOCK = threading.RLock()
BUTTON_LOCK = threading.RLock()
CHAT_FILTERS = {}

# Connection
CHAT_ACCESS_LOCK = threading.RLock()
CONNECTION_INSERTION_LOCK = threading.RLock()
CONNECTION_HISTORY_LOCK = threading.RLock()
HISTORY_CONNECT = {}

# Disable
DISABLE_INSERTION_LOCK = threading.RLock()
DISABLED = {}

# Locks
PERM_LOCK = threading.RLock()
RESTR_LOCK = threading.RLock()

# Notes
NOTES_INSERTION_LOCK = threading.RLock()
BUTTONS_INSERTION_LOCK = threading.RLock()

# Purges
PURGES_INSERTION_LOCK = threading.RLock()

# Report
CHAT_LOCK = threading.RLock()
USER_LOCK = threading.RLock()

# for afk, uinfo, users
INSERTION_LOCK = threading.RLock()
