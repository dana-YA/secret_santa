from werkzeug.exceptions import NotFound, BadRequest

from app.dao.participant import ParticipantDAO
from app.dao.participant_preference import ParticipantPreferenceDAO
from app.helpers.enums import ParticipantPreferenceType
from app.services.user import UserService


class ParticipantService:
    @staticmethod
    def create_participants(event_id: int, participants_data: list):
        """
        Create multiple participants for an event.
        If a user does not exist, create a new user.
        """
        participants = []
        for data in participants_data:
            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            # Check if the user already exists
            user = UserService.upsert_user(email, first_name, last_name)

            # Create a participant for the event
            participant = ParticipantDAO.create_participant(
                user_id=user.id, event_id=event_id
            )
            participants.append(participant.serialize)

        return participants

    @staticmethod
    def add_participant_preference(
        event_id: int,
        participant_id: int,
        target_participant_id: int,
        preference_type=ParticipantPreferenceType.AVOID,
    ):
        """
        Add a preference for a participant.
        """

        # Check if the participant and target participant belong to the same event
        participant = ParticipantDAO.get(participant_id)
        target_participant = ParticipantDAO.get(target_participant_id)

        if not participant or not target_participant:
            raise NotFound("Participant or target participant not found")

        if participant.event_id != event_id or target_participant.event_id != event_id:
            raise BadRequest(
                "Participant and target participant must belong to the same event"
            )

        # Create the preference
        preference = ParticipantPreferenceDAO.create_preference(
            participant_id=participant_id,
            target_participant_id=target_participant_id,
            preference_type=preference_type,
        )
        return preference
