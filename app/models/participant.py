from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseModel as Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    user = relationship("User", backref="participations")
    event = relationship("Event", back_populates="participants")

    preferences = relationship(
        "ParticipantPreference",
        foreign_keys="[ParticipantPreference.participant_id]",
        back_populates="participant",
        cascade="all, delete-orphan",
    )

    gifter_pairings = relationship(
        "EventPairing",
        foreign_keys="[EventPairing.gifter_participant_id]",
        back_populates="santa",
        cascade="all, delete-orphan",
    )

    recipient_pairings = relationship(
        "EventPairing",
        foreign_keys="[EventPairing.recipient_participant_id]",
        back_populates="recipient",
        cascade="all, delete-orphan",
    )

    @property
    def serialize(self):
        """
        :return: an object data in easily serializable format
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
        }
