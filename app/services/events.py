from werkzeug.exceptions import BadRequest, NotFound

from app.dao.event import EventDAO
from app.dao.participant import ParticipantDAO

from app.services.event_pairing import EventPairingService


class EventService:

    def create(
        user_id: int, name: str, event_date, budget: float, currency: str = "EUR"
    ):

        if EventDAO.get_by_name(user_id, name):
            raise BadRequest("Event with Name already exists")

        event = EventDAO.create(user_id, name, event_date, budget, currency)
        return event.serialize

    def get(event_id: int):

        event = EventDAO.get(event_id)

        if not event:
            raise NotFound("Event not found")

        return event

    def generate_pairings(event_id: int):

        event = EventDAO.get(event_id)

        if not event:
            raise NotFound("Event not found")

        event_participants = ParticipantDAO.get_event_participants(event_id)

        event_pairings = EventPairingService.pair_participants(event_participants)

        if not event_pairings:
            raise BadRequest("Event pairing not possible")

        EventDAO.set_event_pairings(event_id, event_pairings)

        # # delete older mathces
        EventDAO.delete_older_events(event.creator_user_id)

        return event_pairings
