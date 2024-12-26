from flask import Flask, render_template, flash, url_for, session, request, redirect

app = Flask(__name__)
app,secret_key =

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
