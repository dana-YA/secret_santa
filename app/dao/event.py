from sqlalchemy import desc, nulls_last
from datetime import datetime

from app.models import Session, Event
from app.dao.event_pairing import EventPairingDAO

MAX_EVENTS_TO_STORE = 5


class EventDAO:
    @staticmethod
    def create(creator_user_id, name, event_date, budget, currency):
        with Session() as session:
            event = Event(
                creator_user_id=creator_user_id,
                name=name,
                event_date=event_date,
                budget=budget,
                currency=currency,
            )
            session.add(event)
            session.commit()
            return event

    @staticmethod
    def get(event_id: int):
        with Session() as session:
            return session.query(Event).filter_by(id=event_id).first()

    @staticmethod
    def get_by_name(creator_user_id: int, name: str):
        with Session() as session:
            return (
                session.query(Event)
                .filter_by(name=name, creator_user_id=creator_user_id)
                .first()
            )

    @staticmethod
    def set_event_pairings(event_id: int, event_pairings: dict):
        EventPairingDAO.delete_old_pairings(event_id)
        EventPairingDAO.add_pairings(event_id, event_pairings)

        # update event pairing date
        with Session() as session:
            session.query(Event).filter_by(id=event_id).update(
                {"pairing_generation_date": datetime.now()}
            )
            session.commit()

    @staticmethod
    def update_user_password(user, new_password_hash):
        with Session() as session:
            user.password_hash = new_password_hash
            session.commit()

    @staticmethod
    def delete_older_events(creator_user_id):
        with Session() as session:
            user_events = (
                session.query(Event)
                .filter_by(creator_user_id=creator_user_id)
                .order_by(
                    nulls_last(desc(Event.pairing_generation_date)), desc(Event.id)
                )
                .all()
            )
            for event in user_events[MAX_EVENTS_TO_STORE:]:
                session.delete(event)
            session.commit()
