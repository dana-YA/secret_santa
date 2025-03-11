from flask_restx import fields, Namespace

ns = Namespace("Participant", description="User operations")

participant_model = ns.model(
    "Participant",
    {
        "email": fields.String(required=False),
        "first_name": fields.String(required=False),
        "last_name": fields.String(required=False),
    },
)


participants_list = ns.model(
    "ParticipantsList", {"participants": fields.List(fields.Nested(participant_model))}
)

participant_preference = ns.model(
    "Participant Prefernece",
    {
        "target_participant_id": fields.Integer(required=True),
    },
)


event_request = ns.model(
    "Event",
    {
        "user_id": fields.Integer(required=True),
        "name": fields.String(required=True),
        "event_date": fields.Date(required=False),
        "budget": fields.Float(required=False),
        "currency": fields.String(required=False),
    },
)
