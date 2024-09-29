from app.packages.auth.models.User import User

class UserRepository:
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def find_by_id(id):
        return User.query.filter_by(id=id).first()
