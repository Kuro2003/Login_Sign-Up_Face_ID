from app.packages.auth.models.User import User

class UserRepository:
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
