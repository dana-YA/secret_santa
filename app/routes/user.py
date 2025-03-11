from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import create_access_token
from app.services.user import UserService
from app.schemas.user import register_model, login_model


ns = Namespace("User", description="User operations", path="/api/user")


class Register(Resource):
    @ns.expect(register_model)
    def post(self):
        data = request.get_json()
        try:
            user = UserService.create_user(
                email=data["email"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            return {"message": "User registered successfully", "user_id": user.id}, 201
        except Exception as e:  # Updated exception
            return {"message": e.message}, e.status_code


ns.add_resource(Register, "/register", methods=["POST"])


class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.get_json()
        try:
            user = UserService.login_user(
                email=data["email"], password=data["password"]
            )
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200
        except Exception as e:  # Updated exception
            return {"message": e.message}, e.status_code


ns.add_resource(Login, "/login", methods=["POST"])
