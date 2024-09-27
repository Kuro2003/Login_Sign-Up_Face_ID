from flask import Flask, redirect, url_for, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cuongnc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route("/")
def hello():
    return render_template('home/home.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # session.permanent = True
        
        if User.query.filter_by(email=email, password=password).first():
            return redirect(url_for('user', email=email, password=password))
        else:
            return "User does not exist"
    return render_template('login/login.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session.permanent = True
        
        found_user = User.query.filter_by(email=email).first()
        
        if found_user:
            return "User already exists"
        else:
            if email and password:
                session['user'] = [email, password]
                user = User(email, password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('user', email=email, password=password))
            else:
                return "email or password is missing"
        
    return render_template('signup/signup.html')
        

@app.route("/user")
def user():
    if "user" in session:
        email, password = session["user"]
        return render_template('user.html', email=email, password=password)
    else:
        return redirect(url_for('login'))

@app.route("/admin")
def hello_admin():
    return "Hello Admin!"

if __name__ == "__main__":
    if not os.path.exists("user.db"):
        with app.app_context():
            db.create_all()
            print("Database created")
    app.run(debug=True)