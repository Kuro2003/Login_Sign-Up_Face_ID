import face_recognition
import numpy as np
import cv2
from app.repositories.UserRepository import UserRepository
from app.config.Database import userdb
from flask import session
from app.packages.auth.models.User import User

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
        # Kiểm tra xem email đã được đăng ký chưa
        user = UserRepository.find_by_email(email)
        
        if user:
            return {"error": "Email already registered"}, 400
        
        # Tạo user mới
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        userdb.session.add(new_user)
        userdb.session.commit()
        
        return {"message": "User registered successfully"}, 201
    
    @staticmethod
    def save_face_id(image_path, user_id):
        # Tìm user bằng id
        user = UserRepository.find_by_id(user_id)
        
        # Nếu không tìm thấy user
        if not user:
            return 400
        
        # Sử dụng face_recognition để tải ảnh trực tiếp thay vì cv2.imread
        image = face_recognition.load_image_file(image_path)
        
        # Lấy face encoding từ ảnh
        encodings = face_recognition.face_encodings(image)

        # Kiểm tra kết quả face_encodings
        if len(encodings) == 0:
            print("No face found in image")
            return 400  # Trả về lỗi nếu không có khuôn mặt
        
        face_encoding = encodings[0]  # Lấy face encoding đầu tiên (nếu có nhiều khuôn mặt)
        
        # Lưu face encoding vào DB
        user.face_encoding = face_encoding.tobytes()  # Chuyển encoding sang dạng byte để lưu vào CSDL
        
        userdb.session.commit()
        
        return 200  # Trả về thành công nếu lưu được face ID

    @staticmethod
    def authenticate_by_face(image_path):
        # Sử dụng face_recognition để tải ảnh trực tiếp thay vì cv2.imread
        image = face_recognition.load_image_file(image_path)

        # Chuyển ảnh về RGB nếu cần (face_recognition sẽ tự động xử lý)
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) == 0:
            print("No face found in image for authentication")
            return None
        
        face_encoding = face_encodings[0]
        
        # Lấy tất cả users từ database
        users = User.query.all()
        
        for user in users:
            if user.face_encoding:
                stored_face_encoding = np.frombuffer(user.face_encoding, dtype=np.float64)
                
                # So sánh khuôn mặt
                result = face_recognition.compare_faces([stored_face_encoding], face_encoding)
                
                if result[0]:  # Kết quả so khớp khuôn mặt
                    return user
        
        return None  # Không tìm thấy user nào khớp với khuôn mặt
