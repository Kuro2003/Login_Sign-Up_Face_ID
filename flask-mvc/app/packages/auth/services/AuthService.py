from app.repositories.UserRepository import UserRepository
from flask import session
from app.packages.auth.models.User import User
from app.config.Database import userdb
import face_recognition
import numpy as np

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
    
    # Hàm lưu ảnh khuôn mặt vào DB
    @staticmethod
    def save_face_id(image_path, user_id):
        user = UserRepository.find_by_id(user_id)
        
        if not user:
            return {"error": "User not found"}, 404
        
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        
        user.face_encoding = face_encoding.tobytes()
        userdb.session.commit()
        
        return {"message": "Face encoding saved successfully"},
    
    # Hàm kiểm tra khuôn mặt khi đăng nhập
    @staticmethod
    def authenticate_by_face(image_path):
        # Đọc ảnh từ file
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        
        users = User.query.all()
        for user in users:
            if user.face_encoding:
                # Chuyển face_encoding từ bytes về numpy array để so sánh
                stored_face_encoding = np.frombuffer(user.face_encoding, dtype=np.float64)
                
                result = face_recognition.compare_faces([stored_face_encoding], face_encoding)
            
                if result[0]: # Nếu khuôn mặt trùng khớp
                    return user
        return None
