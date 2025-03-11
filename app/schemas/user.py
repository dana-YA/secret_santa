from flask_restx import fields, Namespace


ns = Namespace("User", description="User operations")

register_model = ns.model(
    "Register",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
    },
)

login_model = ns.model(
    "Login",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

change_password_model = ns.model(
    "ChangePassword",
    {
        "old_password": fields.String(required=True),
        "new_password": fields.String(required=True),
    },
)
