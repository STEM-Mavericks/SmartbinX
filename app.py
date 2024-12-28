from flask import Flask, render_template, flash, url_for, session, request, redirect
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Ensure SECRET_KEY is loaded correctly from .env file
db = SQLAlchemy(app)

# Username and Password validation functions
def validate_username(username):
    return len(username) >= 3 and len(username) <= 20

def validate_password(password):
    return len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password)

# Routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to log in to access the dashboard.', 'warning')
        return redirect(url_for('auth'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        # Handle Login
        if action == 'login':
            if not username or not password:
                flash('Username and Password are required.', 'danger')
                return redirect(url_for('auth'))
            
            if username in users and check_password_hash(users[username], password):
                session['username'] = username
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
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
            elif username in users:
                flash('This username is already taken. Please choose another.', 'danger')
            else:
                # Register the new user
                users[username] = generate_password_hash(password)
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('auth'))  # Redirect to the login page after successful registration

    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth')) 

if __name__ == '__main__':
    app.run(debug=True)
