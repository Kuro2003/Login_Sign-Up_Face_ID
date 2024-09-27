from app.repositories.UserRepository import UserRepository
from flask import session
from app.packages.auth.models.User import User
from app.config.userdb import db

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        user = UserRepository.find_by_email(email)
        if user and user.check_password(password):
            session['user_id'] = user.id
            return user
        return None
    
    @staticmethod
    def register_user(email, password):
        user = UserRepository.find_by_email(email)
        
        if user:
            return {"error": "Email already registered"}, 400
        
        # Tạo user mới
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201
