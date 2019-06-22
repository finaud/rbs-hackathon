from flask import Flask, render_template, flash, session, redirect, url_for, request
from requests import HTTPError
from datetime import timedelta

import pyrebase

import config

app = Flask(__name__)
app.secret_key = config.secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

firebase = pyrebase.initialize_app(config.pyrebase)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email, password = request.form['email'], request.form['password']
            user = firebase.auth().create_user_with_email_and_password(email, password)
            session['token'] = user['idToken']
            session['user_id'] = user['localId']

            flash("Account created", "message")

            return redirect(url_for('bucket'))

        except HTTPError:
            flash("Try again (email already in use, or use a stronger password)", "error")
            return render_template('auth/register.html')

    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email, password = request.form['email'], request.form['password']
            user = firebase.auth().sign_in_with_email_and_password(email, password)
            session['token'] = user['idToken']
            session['user_id'] = user['localId']

            flash("Login successful", "message")

            return redirect(url_for('bucket'))

        except HTTPError:
            flash("Try again (invalid email or password)", "error")
            return render_template('auth/login.html')

    return render_template('auth/login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash("You have been logged out", "message")
    return render_template('index.html')


@app.route('/promises', methods=['GET'])
def promises():
    if 'token' not in session:
        return redirect(url_for('login'))
    items = firebase.database().child(session['user_id']).get()
    promises = []
    if items.val():
        for item in items.each():
            promises.append({'item_id': item.key(), 'goal': item.val()['goal']})

    return render_template('promises/main.html', promises=promises)


@app.route('/create_promise', methods=['GET', 'POST'])
def create_promise():
    if 'token' not in session:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        promise = request.form['promise']
        data = {'promise': promise}
        firebase.database().child(session['user_id']).push(data)
        return redirect(url_for('promises'))

    return render_template('promises/create_promise.html')


@app.route('/invitation', methods=['GET'])
def invitation():
    return render_template('invitation.html')
