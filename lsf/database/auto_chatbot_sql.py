import threading

from sqlalchemy import Column, String

from . import BASE, SESSION


class LynxChats(BASE):
    __tablename__ = "lynx_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


LynxChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_lynx(chat_id):
    try:
        chat = SESSION.query(LynxChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_lynx(chat_id):
    with INSERTION_LOCK:
        lynxchat = SESSION.query(LynxChats).get(str(chat_id))
        if not lynxchat:
            lynxchat = LynxChats(str(chat_id))
        SESSION.add(lynxchat)
        SESSION.commit()


def rem_lynx(chat_id):
    with INSERTION_LOCK:
        lynxchat = SESSION.query(LynxChats).get(str(chat_id))
        if lynxchat:
            SESSION.delete(lynxchat)
        SESSION.commit()


def get_all_lynx_chats():
    try:
        return SESSION.query(LynxChats.chat_id).all()
    finally:
        SESSION.close()
