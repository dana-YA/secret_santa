import unittest
from unittest.mock import patch
from werkzeug.exceptions import BadRequest

from app.services.event_pairing import EventPairingService


class TestEventPairingService(unittest.TestCase):

    def test_pair_participants_success(self):
        """
        Test successful generation of pairings.
        """
        participants = [
            {"id": 1, "preferences": []},
            {"id": 2, "preferences": []},
        ]

        # Call the pair_participants method
        result = EventPairingService.pair_participants(participants)

        # Assertions
        self.assertEqual(len(result), 2)  # There should be 2 pairings

        # Extract all gifter_ids and recipient_ids
        gifter_ids = [pairing["gifter_id"] for pairing in result]
        recipient_ids = [pairing["recipient_id"] for pairing in result]

        # Ensure each participant is a gifter exactly once
        self.assertEqual(sorted(gifter_ids), [1, 2])

        # Ensure each participant is a recipient exactly once
        self.assertEqual(sorted(recipient_ids), [1, 2])

        # Ensure no participant is paired with themselves
        for pairing in result:
            self.assertNotEqual(pairing["gifter_id"], pairing["recipient_id"])

    def test_pair_participants_insufficient_participants(self):
        """
        Test pairing generation with insufficient participants.
        """
        participants = [{"id": 1, "preferences": []}]

        # Call the pair_participants method and expect a BadRequest exception
        with self.assertRaises(BadRequest) as context:
            EventPairingService.pair_participants(participants)

        # Assertions
        self.assertEqual(
            str(context.exception),
            "400 Bad Request: Not enough participants to generate pairings",
        )

    def test_pair_participants_failure_due_to_constraints(self):
        """
        Test pairing generation failure due to constraints.
        """
        participants = [
            {"id": 1, "preferences": [{"target_participant_id": 2}]},
            {"id": 2, "preferences": [{"target_participant_id": 1}]},
        ]

        # Call the pair_participants method and expect a BadRequest exception
        with self.assertRaises(BadRequest) as context:
            EventPairingService.pair_participants(participants)

        # Assertions
        self.assertEqual(
            str(context.exception),
            "400 Bad Request: Failed to generate pairings after 5 attempts",
        )

    def test_pair_participants_each_matched_once(self):
        """
        Test that with 4 participants, each is matched exactly once as a gifter and once as a recipient.
        """
        participants = [
            {"id": 1, "preferences": []},
            {"id": 2, "preferences": []},
            {"id": 3, "preferences": []},
            {"id": 4, "preferences": []},
        ]

        # Call the pair_participants method
        result = EventPairingService.pair_participants(participants)

        # Assertions
        self.assertEqual(len(result), 4)  # There should be 4 pairings

        # Extract all gifter_ids and recipient_ids
        gifter_ids = [pairing["gifter_id"] for pairing in result]
        recipient_ids = [pairing["recipient_id"] for pairing in result]

        # Ensure each participant appears exactly once as a gifter and once as a recipient
        self.assertEqual(sorted(gifter_ids), [1, 2, 3, 4])
        self.assertEqual(sorted(recipient_ids), [1, 2, 3, 4])

        # Ensure no participant is paired with themselves
        for pairing in result:
            self.assertNotEqual(pairing["gifter_id"], pairing["recipient_id"])


if __name__ == "__main__":
    unittest.main()
