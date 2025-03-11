from flask import jsonify
from werkzeug.exceptions import HTTPException


class CustomException(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def register_error_handlers(app):
    """
    Register custom error handlers for the Flask app.
    """

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Handle HTTP exceptions (e.g., 404, 500)
        if isinstance(e, HTTPException):
            return (
                jsonify(
                    {
                        "message": e.description,
                    }
                ),
                e.code,
            )

        # Handle custom exceptions
        if hasattr(e, "message") and hasattr(e, "status_code"):
            return (
                jsonify(
                    {
                        "message": e.message,
                    }
                ),
                e.status_code,
            )

        # Handle all other exceptions
        return (
            jsonify(
                {
                    "message": "An unexpected error occurred.",
                }
            ),
            500,
        )
