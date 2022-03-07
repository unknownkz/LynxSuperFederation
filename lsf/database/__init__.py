import atexit
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from .. import DATABASE_URL
from .. import LOGGER as LSF_LOGS

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


def start() -> scoped_session:
    machine = create_engine(DATABASE_URL, echo=True)
    LSF_LOGS.info("[PostgreSQL] Connecting to database...")
    BASE.metadata.bind = machine
    BASE.metadata.create_all(machine, checkfirst=True)
    return scoped_session(sessionmaker(bind=machine, autoflush=True, autocommit=False, expire_on_commit=True))


try:
    BASE = declarative_base()
    SESSION = start()
    LSF_LOGS.info("[PostgreSQL] Connection successfully, session started.")
    SESSION.commit()
    sys.stdout.flush()
    atexit.register(SESSION)

except Exception as e:
    LSF_LOGS.exception(f"[PostgreSQL] Failed to connect due to {e}")


finally:
    SESSION.close()
