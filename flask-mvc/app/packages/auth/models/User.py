from app.config.Database import userdb
from flask_bcrypt import generate_password_hash, check_password_hash

class User(userdb.Model):
    first_name = userdb.Column(userdb.String(150), nullable=False)
    last_name = userdb.Column(userdb.String(150), nullable=False)
    id = userdb.Column(userdb.Integer, primary_key=True)
    email = userdb.Column(userdb.String(150), unique=True, nullable=False)
    password = userdb.Column(userdb.String(150), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # Mã hóa mật khẩu trước khi lưu vào DB
        self.password = generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
