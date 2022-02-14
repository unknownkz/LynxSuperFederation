import threading

from sqlalchemy import func, distinct, Column, String, UnicodeText, BigInteger
from . import SESSION, BASE


class BlackListFilters(BASE):
    __tablename__ = "blacklist"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, trigger):
        self.chat_id = str(chat_id)  # ensure string
        self.trigger = trigger

    def __repr__(self):
        return "<Blacklist filter '%s' for %s>" % (self.trigger, self.chat_id)

    def __eq__(self, other):
        return bool(
            isinstance(other, BlackListFilters)
            and self.chat_id == other.chat_id
            and self.trigger == other.trigger
        )


class BlacklistSettings(BASE):
    __tablename__ = "blacklist_settings"
    chat_id = Column(String(14), primary_key=True)
    blacklist_type = Column(BigInteger, default=1)
    value = Column(UnicodeText, default="0")

    def __init__(self, chat_id, blacklist_type=1, value="0"):
        self.chat_id = str(chat_id)
        self.blacklist_type = blacklist_type
        self.value = value

    def __repr__(self):
        return "<{} will executing {} for blacklist trigger.>".format(
            self.chat_id, self.blacklist_type
        )


BlackListFilters.__table__.create(checkfirst=True)
BlacklistSettings.__table__.create(checkfirst=True)

BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()
BLACKLIST_SETTINGS_INSERTION_LOCK = threading.RLock()

CHAT_SETTINGS_BLACKLISTS = {}
CHAT_BLACKLISTS = {
   "tmo",
   "teemo",
   "temeho",
   "giveaway",
   "j.o.i.n",
   "battle roasting",
   "teemoo",
   "b.i.o",
   "opmem",
   "T.M.O",
   "biyo",
   "dibeo",
   "dibiyo",
   "𝐋𝐈𝐍𝐊",
   "ʟɪɴᴋ",
   "𝐎𝐏𝐄𝐍",
   "tm00",
   "𝐛𝐢𝐨",
   "𝘣𝘪𝘰",
   "🅛🅘🅝",
   "tmo",
   "ⓣⓜⓞ",
   "𝗧𝗺𝗼",
   "𝐓𝐌𝐎",
   "𝑻𝑴𝑶",
   "🅣🅜🅞",
   "ᴛᴍᴏ",
   "open vcs",
   "vicies",
   "TAKEE ME OUT",
   "ttteeeeemmmmmoooooo",
   "tttteeemmmmmooohhh",
   "teeeeeemooooohhhh",
   "ᴛᴇᴇᴍᴍᴏᴏʜʜ+ɢɪᴘᴇᴡᴀʏ",
   "tttttmmmmmoooooo",
   "𝐓𝐄𝐄𝐄𝐌𝐌𝐌𝐄𝐄𝐎𝐎𝐎𝐇𝐇𝐇",
   ".delayspam",
   "!delayspam",
   "$delayspam",
   ".admins",
   ".staff",
   "!admins",
   "!staff",
   "$staff",
   "/admins",
   "/staff",
   "tmeho+cuan",
   "tmhogipewe",
   "TEME0",
   "B1Y0",
   "ᴛ.ᴍ.ᴏ",
   "b1yo",
   "biy0",
   "b,io",
   "Teeeemoooo",
   "dibeoo",
   "𝗰𝗲𝗸 𝗲𝗯𝘆𝗼𝘂𝗵𝗵",
   "𝐓𝐄𝐌𝐄𝐇𝐎",
   "𝐁𝐈𝐇𝐎",
   "gipewe",
   "ɢɪᴘᴇᴡᴇ",
   "ᴛᴇᴍᴇʜᴏ",
   "openvcbugilcolmekyuuksayang",
   "ᴛᴇᴋᴋᴍɪɪᴏᴏᴏᴛᴛᴛᴛᴛᴛ",
   "mauchat18pluss",
   "opnvcsperbayar",
   "sangenivcsdong",
   "teeemmmoohhhhh",
   "tengmohhhhhhh",
   "bioooohhhhhh",
   "sleepchat💦💦💦",
   "call💦💦",
   "💦",
   "teengmoooooo",
   "tekmioooottt",
   "tekmiottttt",
   "🆃🅼🅾+🅶🅸🅿🅴🆆🅴🆈",
   "🆃🅼🅾",
   "🅶🅸🅿🅴🆆🅴🆈",
   "🅣🅜🅞🅛🅘🅝🅓🅘🅑🅘🅞",
   "beohhhhhhh",
   "/delayspam",
   "opnnvcssss",
   "sange",
   "lagiange",
   "teeeekmiaw",
   "tmhhhhoooo",
   "0penadmin",
   "biyowwwww",
   "𝐛𝐢𝐲𝐲𝐲𝐨𝐨𝐨🥵",
   "delayspam",
   "gipewayyy",
   "gipeweyyy",
   "opencsvcs",
   "opnnvcsss",
   "teemeeooo",
   "teemohhhh",
   "temmmoooh",
   "ᴛᴇᴇᴍᴍᴏᴏʜʜ",
   "angggeee",
   "biohhhhh",
   "dibiyyoo",
   "teemeeoo",
   "teemmooo",
   "𝐭𝐞𝐞𝐦𝐨𝐡𝐡𝐡",
   "teemoohh",
   "𝙏𝙀𝙈𝙀𝙃𝙊𝙀𝙏",
   "ve.ce.es",
   "becekin",
   "𝚋𝚎𝚒𝚢𝚘𝚘𝚑",
   "biyhooo",
   "byooohh",
   "ʙɪʏʏᴏᴏᴏ",
   "colm**k",
   "desahan",
   "desahin",
   "dibeioo",
   ".filter",
   "!filter",
   "$filter",
   ",delayspam",
   ",.delayspam",
   ",filter",
   ",.filter",
   "jowinnn",
   "𝗟𝗜𝗣𝗦𝗛𝗢𝗪",
   "𝐦𝐚𝐧𝐭𝐚𝐩2",
   "ngentot",
   "ngentod",
   "premium",
   "tallent",
   "𝘛𝘌𝘌𝘔𝘖𝘏𝘏",
   "temiohh",
   "temoooo",
   "tmoooo",
   "v.i.d🔞😘",
   "biyyoo",
   "angee",
   "ange",
   "biyyoo",
   "callsx",
   "colbar",
   "colmek",
   "grepeh",
   "kebio",
   "kebiioe",
   "kontol",
   "ngisep",
   "ngoco*",
   "pideo*",
   "sangeet",
   "sangek",
   "shange",
   "t33mho",
   "𝕋𝕒𝕝𝕖𝕟𝕥",
   "ᵀᴱᴹᴱᴴᴼ",
   "𝙏𝙀𝙈𝙊𝙃𝙃",
   "timiho",
   "t.me/*",
   "🆃︎🅼︎🅾︎",
   "╟◈",
   "vc$",
   "p©$",
   "/id",
   "opn",
   "pc💦",
   "𝐓𝐌𝐎",
   "𝙏𝙈𝙊",
   "𝚃𝙼𝙾",
   "𝘛𝘔𝘖",
   "𝑻𝑴𝑶",
   "open war",
   "TEKMEOT",
}

def add_to_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = BlackListFilters(str(chat_id), trigger)

        SESSION.merge(blacklist_filt)  # merge to avoid duplicate key issues
        SESSION.commit()
        global CHAT_BLACKLISTS
        if CHAT_BLACKLISTS.get(str(chat_id), set()) == set():
            CHAT_BLACKLISTS[str(chat_id)] = {trigger}
        else:
            CHAT_BLACKLISTS.get(str(chat_id), set()).add(trigger)


def rm_from_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = SESSION.query(BlackListFilters).get((str(chat_id), trigger))
        if blacklist_filt:
            if trigger in CHAT_BLACKLISTS.get(str(chat_id), set()):  # sanity check
                CHAT_BLACKLISTS.get(str(chat_id), set()).remove(trigger)

            SESSION.delete(blacklist_filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def get_chat_blacklist(chat_id):
    return CHAT_BLACKLISTS.get(str(chat_id), set())


def num_blacklist_filters():
    try:
        return SESSION.query(BlackListFilters).count()
    finally:
        SESSION.close()


def num_blacklist_chat_filters(chat_id):
    try:
        return (
            SESSION.query(BlackListFilters.chat_id)
            .filter(BlackListFilters.chat_id == str(chat_id))
            .count()
        )
    finally:
        SESSION.close()


def num_blacklist_filter_chats():
    try:
        return SESSION.query(func.count(distinct(BlackListFilters.chat_id))).scalar()
    finally:
        SESSION.close()


def set_blacklist_strength(chat_id, blacklist_type, value):
    # for blacklist_type
    # 0 = nothing
    # 1 = delete
    # 2 = warn
    # 3 = mute
    # 4 = kick
    # 5 = ban
    # 6 = tban
    # 7 = tmute
    with BLACKLIST_SETTINGS_INSERTION_LOCK:
        global CHAT_SETTINGS_BLACKLISTS
        curr_setting = SESSION.query(BlacklistSettings).get(str(chat_id))
        if not curr_setting:
            curr_setting = BlacklistSettings(
                chat_id, blacklist_type=int(blacklist_type), value=value
            )

        curr_setting.blacklist_type = int(blacklist_type)
        curr_setting.value = str(value)
        CHAT_SETTINGS_BLACKLISTS[str(chat_id)] = {
            "blacklist_type": int(blacklist_type),
            "value": value,
        }

        SESSION.add(curr_setting)
        SESSION.commit()


def get_blacklist_setting(chat_id):
    try:
        setting = CHAT_SETTINGS_BLACKLISTS.get(str(chat_id))
        if setting:
            return setting["blacklist_type"], setting["value"]
        else:
            return 1, "0"

    finally:
        SESSION.close()


def __load_chat_blacklists():
    global CHAT_BLACKLISTS
    try:
        chats = SESSION.query(BlackListFilters.chat_id).distinct().all()
        for (chat_id,) in chats:  # remove tuple by ( ,)
            CHAT_BLACKLISTS[chat_id] = []

        all_filters = SESSION.query(BlackListFilters).all()
        for x in all_filters:
            CHAT_BLACKLISTS[x.chat_id] += [x.trigger]

        CHAT_BLACKLISTS = {x: set(y) for x, y in CHAT_BLACKLISTS.items()}

    finally:
        SESSION.close()


def __load_chat_settings_blacklists():
    global CHAT_SETTINGS_BLACKLISTS
    try:
        chats_settings = SESSION.query(BlacklistSettings).all()
        for x in chats_settings:  # remove tuple by ( ,)
            CHAT_SETTINGS_BLACKLISTS[x.chat_id] = {
                "blacklist_type": x.blacklist_type,
                "value": x.value,
            }

    finally:
        SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        chat_filters = (
            SESSION.query(BlackListFilters)
            .filter(BlackListFilters.chat_id == str(old_chat_id))
            .all()
        )
        for filt in chat_filters:
            filt.chat_id = str(new_chat_id)
        SESSION.commit()


__load_chat_blacklists()
__load_chat_settings_blacklists()