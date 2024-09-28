from flask import Blueprint, request, jsonify
from app.packages.auth.services.AuthService import AuthService   

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
    
    return AuthService.register_user(first_name,last_name, email, password)
        