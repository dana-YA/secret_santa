from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr, declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        index=True,
    )
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), index=True
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
