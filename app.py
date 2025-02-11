from flask import Flask, render_template, flash, url_for, session, request, redirect
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_HOST')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class WasteRecord(db.Model):
    __tablename__ = 'waste_records'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    dry_weight = db.Column(db.Float, nullable=False, default=0.0)  # In kg
    wet_weight = db.Column(db.Float, nullable=False, default=0.0)  # In kg
    total_weight = db.Column(db.Float, nullable=False, default=0.0)  # Dry + Wet

    def __init__(self, date, dry_weight, wet_weight):
        self.date = date
        self.dry_weight = dry_weight
        self.wet_weight = wet_weight
        self.total_weight = dry_weight + wet_weight

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def validate_username(username):
    return 3 <= len(username) <= 20

def validate_password(password):
    return len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        if action == 'login':
            if not username or not password:
                flash('Username and Password are required.', 'danger')
                return redirect(url_for('auth'))

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password. Please try again.', 'danger')
                return redirect(url_for('auth'))

        elif action == 'register': 
            if not username or not password:
                flash('Username and Password are required for registration.', 'danger')
            elif not validate_username(username):
                flash('Username must be between 3 and 20 characters.', 'danger')
            elif not validate_password(password):
                flash('Password must be at least 8 characters long, contain a number, and an uppercase letter.', 'danger')
            elif User.query.filter_by(username=username).first():
                flash('This username is already taken. Please choose another.', 'danger')
            else:
                hashed_password = generate_password_hash(password)
                new_user = User(name=username, username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('auth'))

    return render_template('auth.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    env = os.getenv('FLASK_ENV', 'production')
    app.run(debug=(env == 'development'))
