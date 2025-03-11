from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base_model import BaseModel as Base


class EventPairing(Base):
    __tablename__ = "event_pairings"

    id = Column(Integer, primary_key=True)
    gifter_participant_id = Column(
        Integer, ForeignKey("participants.id"), nullable=False
    )
    recipient_participant_id = Column(
        Integer, ForeignKey("participants.id"), nullable=False
    )
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    santa = relationship(
        "Participant",
        foreign_keys=[gifter_participant_id],
        back_populates="gifter_pairings",
    )
    recipient = relationship(
        "Participant",
        foreign_keys=[recipient_participant_id],
        back_populates="recipient_pairings",
    )
    event = relationship("Event", backref="pairings")

    # Unique constraint to prevent duplicate pairings
    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "gifter_participant_id",
            "recipient_participant_id",
            name="uq_event_gifter_recipient",
        ),
    )
