import threading

from sqlalchemy import Column, String, BigInteger

from . import BASE, SESSION


class Agreedals(BASE):
    __tablename__ = "agreecheck"
    chat_id = Column(String(14), primary_key=True)
    user_id = Column(BigInteger, primary_key=True)

    def __init__(self, chat_id, user_id):
        self.chat_id = str(chat_id)  # ensure string
        self.user_id = user_id

    def __repr__(self):
        return "<Agree %s>" % self.user_id


Agreedals.__table__.create(checkfirst=True)

AGREE_INSERTION_LOCK = threading.RLock()


def agree(chat_id, user_id):
    with AGREE_INSERTION_LOCK:
        agree_user = Agreedals(str(chat_id), user_id)
        SESSION.add(agree_user)
        SESSION.commit()


def is_agreed(chat_id, user_id):
    try:
        return SESSION.querry(Agreedals).get((str(chat_id), user_id))
    finally:
        SESSION.close()


def disagree(chat_id, user_id):
    with AGREE_INSERTION_LOCK:
        disagree_user = SESSION.query(Agreedals).get((str(chat_id), user_id))
        if disagree_user:
            SESSION.delete(disagree_user)
            SESSION.commit()
            return True
        else:
            SESSION.close()
            return False


def list_agreed(chat_id):
    try:
        return (
            SESSION.query(Agreedals).filter(Agreedals.chat_id == str(chat_id)).order_by(Agreedals.user_id.asc()).all()
        )
    finally:
        SESSION.close()
