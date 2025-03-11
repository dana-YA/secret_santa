from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash
from app.dao.user import UserDAO
from app.helpers.utils import generate_password


class UserService:

    @staticmethod
    def create_user(email, password, first_name, last_name):
        # Check if email already exists
        if UserDAO.get_user_by_email(email):
            raise BadRequest("Email already exists")

        # Hash the password and create the user
        password_hash = generate_password_hash(password)
        try:
            user = UserDAO.create_user(
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
            )
            return user
        except IntegrityError as e:
            # Catch DB-level uniqueness violations
            raise BadRequest(f"Database integrity error: email already exists {e}")

    @staticmethod
    def upsert_user(email, first_name, last_name):
        user = UserDAO.get_user_by_email(email)

        if user:
            return user

        ## Todo: Random Generation of Password & Sending of email for login
        password = generate_password()
        password_hash = generate_password_hash(password)
        user = UserService.create_user(email, password_hash, first_name, last_name)
        return user

    @staticmethod
    def login_user(email, password):
        user = UserDAO.get_user_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            raise BadRequest("Invalid email or password")
        return user

    @staticmethod
    def change_password(user, old_password, new_password):
        if not check_password_hash(user.password_hash, old_password):
            raise BadRequest("Old password is incorrect")
        new_password_hash = generate_password_hash(new_password)
        UserDAO.update_user_password(user, new_password_hash)
