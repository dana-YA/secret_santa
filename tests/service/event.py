import unittest
from unittest.mock import patch, MagicMock
from werkzeug.exceptions import BadRequest, NotFound

from app.services.events import EventService
from app.dao.event import EventDAO
from app.dao.participant import ParticipantDAO
from app.services.event_pairing import EventPairingService


class TestEventService(unittest.TestCase):

    @patch("app.services.events.EventDAO")
    def test_create_event_success(self, mock_event_dao):
        """
        Test successful creation of an event.
        """
        # Mock EventDAO.get_by_name to return None (no existing event with the same name)
        mock_event_dao.get_by_name.return_value = None

        # Mock EventDAO.create to return a mock event
        mock_event = MagicMock()
        mock_event.serialize = {"id": 1, "name": "Test Event", "creator_user_id": 1}
        mock_event_dao.create.return_value = mock_event

        # Call the create method
        result = EventService.create(1, "Test Event", "2023-12-25", 100.0, "EUR")

        # Assertions
        self.assertEqual(result, {"id": 1, "name": "Test Event", "creator_user_id": 1})
        mock_event_dao.get_by_name.assert_called_once_with(1, "Test Event")
        mock_event_dao.create.assert_called_once_with(
            1, "Test Event", "2023-12-25", 100.0, "EUR"
        )

    @patch("app.services.events.EventDAO")
    def test_create_event_duplicate_name(self, mock_event_dao):
        """
        Test creation of an event with a duplicate name.
        """
        # Mock EventDAO.get_by_name to return an existing event
        mock_event_dao.get_by_name.return_value = MagicMock()

        # Call the create method and expect a BadRequest exception
        with self.assertRaises(BadRequest) as context:
            EventService.create(1, "Test Event", "2023-12-25", 100.0, "EUR")

        # Assertions
        self.assertEqual(
            str(context.exception), "400 Bad Request: Event with Name already exists"
        )
        mock_event_dao.get_by_name.assert_called_once_with(1, "Test Event")
        mock_event_dao.create.assert_not_called()

    @patch("app.services.events.EventDAO")
    def test_get_event_success(self, mock_event_dao):
        """
        Test successful retrieval of an event.
        """
        # Mock EventDAO.get to return a mock event
        mock_event = MagicMock()
        mock_event_dao.get.return_value = mock_event

        # Call the get method
        result = EventService.get(1)

        # Assertions
        self.assertEqual(result, mock_event)
        mock_event_dao.get.assert_called_once_with(1)

    @patch("app.services.events.EventDAO")
    def test_get_event_not_found(self, mock_event_dao):
        """
        Test retrieval of a non-existent event.
        """
        # Mock EventDAO.get to return None
        mock_event_dao.get.return_value = None

        # Call the get method and expect a NotFound exception
        with self.assertRaises(NotFound) as context:
            EventService.get(1)

        # Assertions
        self.assertEqual(str(context.exception), "404 Not Found: Event not found")
        mock_event_dao.get.assert_called_once_with(1)

    @patch("app.services.events.ParticipantDAO")
    @patch("app.services.events.EventDAO")
    @patch("app.services.events.EventPairingService")
    def test_generate_pairings_success(
        self, mock_pairing_service, mock_event_dao, mock_participant_dao
    ):
        """
        Test successful generation of pairings.
        """
        # Mock EventDAO.get to return a mock event
        mock_event = MagicMock()
        mock_event.creator_user_id = 1
        mock_event_dao.get.return_value = mock_event

        # Mock ParticipantDAO.get_event_participants to return a list of participants
        mock_participants = [
            {"id": 1, "name": "Alice", "preferences": []},
            {"id": 2, "name": "Bob", "preferences": []},
        ]
        mock_participant_dao.get_event_participants.return_value = mock_participants

        # Mock EventPairingService.pair_participants to return pairings
        mock_pairings = [
            {"gifter_id": 1, "recipient_id": 2},
            {"gifter_id": 2, "recipient_id": 1},
        ]
        mock_pairing_service.pair_participants.return_value = mock_pairings

        # Call the generate_pairings method
        result = EventService.generate_pairings(1)

        # Assertions
        self.assertEqual(result, mock_pairings)
        mock_event_dao.get.assert_called_once_with(1)
        mock_participant_dao.get_event_participants.assert_called_once_with(1)
        mock_pairing_service.pair_participants.assert_called_once_with(
            mock_participants
        )
        mock_event_dao.set_event_pairings.assert_called_once_with(1, mock_pairings)
        mock_event_dao.delete_older_events.assert_called_once_with(1)

    @patch("app.services.events.ParticipantDAO")
    @patch("app.services.events.EventDAO")
    @patch("app.services.events.EventPairingService")
    def test_generate_pairings_not_found(
        self, mock_pairing_service, mock_event_dao, mock_participant_dao
    ):
        """
        Test generation of pairings for a non-existent event.
        """
        # Mock EventDAO.get to return None
        mock_event_dao.get.return_value = None

        # Call the generate_pairings method and expect a NotFound exception
        with self.assertRaises(NotFound) as context:
            EventService.generate_pairings(1)

        # Assertions
        self.assertEqual(str(context.exception), "404 Not Found: Event not found")
        mock_event_dao.get.assert_called_once_with(1)
        mock_participant_dao.get_event_participants.assert_not_called()
        mock_pairing_service.pair_participants.assert_not_called()
        mock_event_dao.set_event_pairings.assert_not_called()
        mock_event_dao.delete_older_events.assert_not_called()

    @patch("app.services.events.ParticipantDAO")
    @patch("app.services.events.EventDAO")
    @patch("app.services.events.EventPairingService")
    def test_generate_pairings_failure(
        self, mock_pairing_service, mock_event_dao, mock_participant_dao
    ):
        """
        Test failure to generate pairings due to constraints.
        """
        # Mock EventDAO.get to return a mock event
        mock_event = MagicMock()
        mock_event.creator_user_id = 1
        mock_event_dao.get.return_value = mock_event

        # Mock ParticipantDAO.get_event_participants to return a list of participants
        mock_participants = [
            {"id": 1, "name": "Alice", "preferences": [{"target_participant_id": 2}]},
            {"id": 2, "name": "Bob", "preferences": [{"target_participant_id": 1}]},
        ]
        mock_participant_dao.get_event_participants.return_value = mock_participants

        # Mock EventPairingService.pair_participants to return None (pairing not possible)
        mock_pairing_service.pair_participants.return_value = None

        # Call the generate_pairings method and expect a BadRequest exception
        with self.assertRaises(BadRequest) as context:
            EventService.generate_pairings(1)

        # Assertions
        self.assertEqual(
            str(context.exception), "400 Bad Request: Event pairing not possible"
        )
        mock_event_dao.get.assert_called_once_with(1)
        mock_participant_dao.get_event_participants.assert_called_once_with(1)
        mock_pairing_service.pair_participants.assert_called_once_with(
            mock_participants
        )
        mock_event_dao.set_event_pairings.assert_not_called()
        mock_event_dao.delete_older_events.assert_not_called()


if __name__ == "__main__":
    unittest.main()
