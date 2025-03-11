from sqlalchemy.orm import joinedload
from app.models import Session, Participant


class ParticipantDAO:

    @staticmethod
    def get(participant_id: int):
        with Session() as session:
            return session.query(Participant).filter_by(id=participant_id).first()

    @staticmethod
    def create_participant(user_id: int, event_id: int):
        with Session() as session:
            participant = Participant(user_id=user_id, event_id=event_id)
            session.add(participant)
            session.commit()
            return participant

    @staticmethod
    def get_event_participants(event_id):
        with Session() as session:
            participants = (
                session.query(Participant)
                .filter(Participant.event_id == event_id)
                .options(joinedload(Participant.preferences))
                .all()
            )

            result = []
            for participant in participants:
                participant_data = participant.serialize
                participant_data["preferences"] = [
                    preference.serialize for preference in participant.preferences
                ]
                result.append(participant_data)

            return result
