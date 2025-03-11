from sqlalchemy import Column, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base_model import BaseModel as Base
from app.helpers.enums import ParticipantPreferenceType  # Ensure this import is correct


class ParticipantPreference(Base):
    __tablename__ = "participant_preferences"

    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    target_participant_id = Column(
        Integer, ForeignKey("participants.id"), nullable=False
    )
    preference_type = Column(Enum(ParticipantPreferenceType), nullable=False)

    # Relationships
    participant = relationship("Participant", foreign_keys=[participant_id])
    target = relationship("Participant", foreign_keys=[target_participant_id])

    # Unique constraint to prevent duplicate preferences
    __table_args__ = (
        UniqueConstraint(
            "participant_id", "target_participant_id", name="unique_participant_target"
        ),
    )

    @property
    def serialize(self):
        """
        :return: an object data in easily serializable format
        """
        return {
            "id": self.id,
            "participant_id": self.participant_id,
            "target_participant_id": self.target_participant_id,
            "preference_type": self.preference_type.value,
        }
