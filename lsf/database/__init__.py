import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from lsf import DATABASE_URL
from lsf import LOGGER as LSF_LOGS

if DATABASE_URL and DATABASE_URL.startswith("mongodb://"):
    DATABASE_URL = DATABASE_URL.replace("mongodb://", "mongodb+srv://", 1)


def start() -> scoped_session:
    engine = create_engine(DATABASE_URL, echo=True)
    LSF_LOGS.info("[PostgreSQL] Connecting to database...")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine, checkfirst=True)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except Exception as e:
    LSF_LOGS.exception(f"[PostgreSQL] Failed to connect due to {e}")
    sys.exit()

LSF_LOGS.info("[PostgreSQL] Connection successful, session started.")

if SESSION is start():
    session.commit()
