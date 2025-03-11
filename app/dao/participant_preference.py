from werkzeug.exceptions import Conflict
from app.models import Session, ParticipantPreference


class ParticipantPreferenceDAO:

    @staticmethod
    def create_preference(participant_id, target_participant_id, preference_type):
        with Session() as session:
            # Check if a preference already exists
            existing_preference = (
                session.query(ParticipantPreference)
                .filter_by(
                    participant_id=participant_id,
                    target_participant_id=target_participant_id,
                    preference_type=preference_type,
                )
                .first()
            )

            if existing_preference:
                raise Conflict("This participant preference already exists.")

            participant_preference = ParticipantPreference(
                participant_id=participant_id,
                target_participant_id=target_participant_id,
                preference_type=preference_type,
            )
            session.add(participant_preference)
            session.commit()
            return participant_preference.serialize
