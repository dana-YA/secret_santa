from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.participants import ParticipantService
from app.services.events import EventService
from app.schemas.events import (
    participants_list,
    participant_preference,
    event_request,
)

ns = Namespace("Event", description="User operations", path="/api/event")


class Event(Resource):
    @jwt_required()
    @ns.expect(event_request)
    def post(self):
        """Create a new event"""
        data = request.get_json()
        user_id = int(get_jwt_identity())

        event = EventService.create(
            user_id=user_id,
            name=data["name"],
            event_date=data["event_date"],
            budget=data["budget"],
            currency=data["currency"],
        )
        return {
            "message": "Event created successfully",
            "data": event,
        }, 201


ns.add_resource(Event, "/", methods=["POST"])


class GeneratePairings(Resource):
    @jwt_required()
    @ns.expect(event_request)
    def post(self, event_id):
        """Generate Event Pairing"""
        event = EventService.generate_pairings(event_id)
        return {
            "message": "Event created successfully",
            "data": event,
        }, 201


ns.add_resource(GeneratePairings, "/<int:event_id>/generate-pairings", methods=["POST"])


class Participant(Resource):
    @jwt_required()
    @ns.expect(participants_list)
    def post(self, event_id: int):
        """Create a new participant or a list of participants"""
        participants = request.get_json()["participants"]

        participants = ParticipantService.create_participants(event_id, participants)
        return {
            "message": "Participants created successfully",
            "data": participants,
        }, 201

    @jwt_required()
    @ns.expect(participant_preference)
    def put(self, event_id, participant_id):
        """Create a new participant or a list of participants"""
        data = request.get_json()
        participants = ParticipantService.add_participant_preference(
            event_id, participant_id, data["target_participant_id"]
        )
        return {
            "message": "Participantupdate successfully",
            "data": participants,
        }, 201


ns.add_resource(Participant, "/<int:event_id>/participants", methods=["POST"])
ns.add_resource(
    Participant,
    "/<int:event_id>/participants/<int:participant_id>/preferences",
    methods=["PUT"],
)
