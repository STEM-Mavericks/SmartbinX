from flask import Flask, render_template, flash, url_for, session, request, redirect
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app,secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
