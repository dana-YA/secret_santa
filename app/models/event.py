from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base_model import BaseModel as Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    creator_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_date = Column(DateTime)
    budget = Column(String)
    currency = Column(String(3), default="EUR")
    pairing_generation_date = Column(DateTime)

    # Relationships
    creator = relationship("User", backref="created_events")
    participants = relationship(
        "Participant", back_populates="event", cascade="all, delete-orphan"
    )

    @property
    def serialize(self):
        """
        :return: an object data in easily serializable format
        """
        return {
            "id": self.id,
            "name": self.name,
            "creator_user_id": self.creator_user_id,
            "budget": self.budget,
            "currency": self.currency,
            "event_date": self.event_date,
        }
