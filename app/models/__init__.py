# flake8: noqa
from sqlalchemy import create_engine
from sqlalchemy.orm import configure_mappers, sessionmaker

from app.config import DB_URI

from .user import User
from .event_pairing import EventPairing
from .event import Event
from .participant_preference import ParticipantPreference
from .participant import Participant
from .base_model import Base


engine = create_engine(
    DB_URI,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
    pool_recycle=3600,
)


# It's important to make this call at this very moment in order to be able to make the database searchable
configure_mappers()

# Create all tables
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
