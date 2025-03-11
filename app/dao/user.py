from app.models import Session, User


class UserDAO:
    @staticmethod
    def get(id: int):
        with Session() as session:
            return session.query(User).filter_by(id=id).first()

    @staticmethod
    def get_user_by_email(email: str):
        with Session() as session:
            return session.query(User).filter_by(email=email).first()

    @staticmethod
    def create_user(email: str, first_name: str, last_name: str, password_hash: str):
        with Session() as session:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=password_hash,
            )
            session.add(user)
            session.commit()
            return user

    @staticmethod
    def update_user_password(user, new_password_hash):
        with Session() as session:
            user.password_hash = new_password_hash
            session.commit()
