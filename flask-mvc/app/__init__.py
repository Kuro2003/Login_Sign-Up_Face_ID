from flask import Flask
from app.packages.auth.controllers.AuthController import auth_blueprint
from app.controllers import *
from flask_sqlalchemy import SQLAlchemy
from app.config.userdb import db
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)
    
    # Cấu hình cho app, bao gồm kết nối database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'cuongnc'
    CORS(app,supports_credentials=True)
    
    # Khởi tạo các thành phần mở rộng
    db.init_app(app)
    
    with app.app_context():
        # Đăng ký các Blueprint hoặc các route khác nếu cần
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        
        # Tạo database nếu cần
        db.create_all()

    return app


