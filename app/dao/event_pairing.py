from app.models import Session, EventPairing


class EventPairingDAO:
    @staticmethod
    def delete_old_pairings(event_id: int):
        with Session() as session:
            session.query(EventPairing).filter(
                EventPairing.event_id == event_id
            ).delete(synchronize_session=False)
            session.commit()

    def add_pairings(event_id: int, event_pairings):
        new_pairings = [
            EventPairing(
                gifter_participant_id=pairing["gifter_id"],
                recipient_participant_id=pairing["recipient_id"],
                event_id=event_id,
            )
            for pairing in event_pairings
        ]

        with Session() as session:
            session.add_all(new_pairings)
            session.commit()
