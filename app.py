from flask import Flask, render_template, flash, url_for, session, request, redirect
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app,secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login Successfull!', 'success')
            return redirect(url_for('login'))
        else
            flash
if __name__ == '__main__':
    app.run(debug=True)
