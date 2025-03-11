from werkzeug.exceptions import BadRequest
import random

MAX_PAIRING_RETRIES = 5


class EventPairingService:
    def _get_preferences(participants):
        """
        Return the list of participants each gifter cannot gift to.

        """
        preferences = {}
        for participant in participants:
            cannot_gift = set(
                preference["target_participant_id"]
                for preference in participant["preferences"]
            )
            preferences[participant["id"]] = cannot_gift
        return preferences

    def _generate_valid_pairings(participants, preferences):
        """
        Greedy pairings for pairs
        """
        pairings = []
        remaining_recipients = set(participant["id"] for participant in participants)

        for gifter in participants:
            # Find a valid recipient for the gifter
            valid_recipients = [
                recipient_id
                for recipient_id in remaining_recipients
                if recipient_id != gifter["id"]
                and recipient_id not in preferences.get(gifter["id"], set())
            ]

            if not valid_recipients:
                return None

            recipient_id = valid_recipients[0]
            pairings.append({"gifter_id": gifter["id"], "recipient_id": recipient_id})
            remaining_recipients.remove(recipient_id)

        return pairings

    def pair_participants(participants: list):

        if len(participants) < 2:
            raise BadRequest("Not enough participants to generate pairings")

        preferences = EventPairingService._get_preferences(participants)

        # Attempt pairing generation up to MAX_PAIRING_RETRIES times
        for attempt in range(MAX_PAIRING_RETRIES):

            random.shuffle(participants)

            pairings = EventPairingService._generate_valid_pairings(
                participants, preferences
            )

            if pairings:
                return pairings

        raise BadRequest("Failed to generate pairings after 5 attempts")
