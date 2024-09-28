from app.repositories.UserRepository import UserRepository
from flask import session
from app.packages.auth.models.User import User
from app.config.Database import userdb

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        user = UserRepository.find_by_email(email)
        if user and user.check_password(password):
            session['user_id'] = user.id
            return user
        return None
    
    @staticmethod
    def register_user(first_name, last_name, email, password):
        user = UserRepository.find_by_email(email)
        
        if user:
            return {"error": "Email already registered"}, 400
        
        # Tạo user mới
        new_user = User(first_name=first_name, last_name=last_name,email=email, password=password)
        userdb.session.add(new_user)
        userdb.session.commit()
        
        return {"message": "User registered successfully"}, 201
