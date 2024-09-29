from flask import Blueprint, request, jsonify
from app.packages.auth.services.AuthService import AuthService   
import uuid
import os

auth_blueprint = Blueprint('auth', __name__)

# Routes: login
@auth_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = AuthService.authenticate_user(email, password)
    
    if user:
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# Routes: register
@auth_blueprint.route('/register', methods=['POST', 'GET'])
def register_user():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    password = request.json.get("password")
    
    if not email or not password:
        return jsonify({"error": "All Fields are required"}), 400
    
    return AuthService.register_user(first_name, last_name, email, password)

@auth_blueprint.route('/register_face', methods=['POST'])
def register_face():
    user_id = request.form.get('user_id')  # Bạn cần xác định user_id từ client
    image_file = request.files.get('image') 
    if image_file is None:
        return jsonify({"message": "No image provided"}), 400
    image_path = f"./app/images/{user_id}.jpg"
    image_file.save(image_path)
    
    AuthService.save_face_id(image_path, user_id)
    
    # Xóa file ảnh sau khi lưu face encoding
    os.remove(image_path)
    
    return jsonify({"message": "Face ID registered successfully"}), 201


@auth_blueprint.route('/login_face', methods=['POST'])
def login_face():
    image_file = request.files.get('image')
    # Tạo tên file ảnh tạm thời dựa trên uuid để tránh ghi đè
    temp_image_path = f"./app/temp_images/{uuid.uuid4()}.jpg"
    image_file.save(temp_image_path)
    
    user = AuthService.authenticate_by_face(temp_image_path)
    
    # Xóa file ảnh tạm sau khi xác thực xong
    os.remove(temp_image_path)
    
    if user:
        return jsonify({"message": "Login successful", "user": user.email}), 200
    else:
        return jsonify({"message": "Face ID does not match"}), 401
