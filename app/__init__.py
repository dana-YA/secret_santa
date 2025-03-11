from flask import Flask, jsonify, request
from flask_restx import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

from app.config import SWAGGER_SCHEME, JWT_KEY
from app.routes.user import ns as user_ns
from app.routes.events import ns as events_ns
from app.schemas.user import ns as user_schema_ns
from app.schemas.events import ns as events_schema_ns
from app.helpers.exceptions import register_error_handlers

# Initialize Flask app
app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = JWT_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

# Swagger Documentation
api = Api(
    app,
    version="1.0",
    title="Secret Santa API",
    doc="/api",  # Swagger UI endpoint
    schemes=[SWAGGER_SCHEME],  # Use the correct scheme (HTTP or HTTPS)
)

register_error_handlers(app)


@app.before_request
def check_api_auth():
    """
    Check JWT token for protected routes, but allow Swagger UI and login routes.
    """
    # Exclude Swagger UI and login routes from JWT check
    excluded_routes = [
        "/api",
        "/api/doc",
        "/api/swagger.json",
        "/api/user/login",
        "/api/user/register",
    ]

    if request.path.startswith("/api") and request.path not in excluded_routes:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid token"}), 401


# Register API routes
api.add_namespace(user_ns)
api.add_namespace(events_ns)
api.add_namespace(user_schema_ns)
api.add_namespace(events_schema_ns)

if __name__ == "__main__":
    app.run(debug=True)
