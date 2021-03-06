from logging import Handler, handlers
import os
import pymysql
from flask import Flask, url_for, request, render_template, redirect, flash, session
from flask.helpers import make_response
from werkzeug.wrappers import response


import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


@app.route('/route')
def hello_route():
    return url_for('show_user', user_id='100')
    # return "Hello route"


@app.route('/users/<user_id>')
def show_user(user_id):
    # show the user_id
    return "Welcome user. Your user_id is "+user_id


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the user_id
    return "This page will show post from id "+str(post_id)


@app.route('/')
@app.route('/<username>')
def index(username="None"):
    return render_template("hello.html", username=username)


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_validate():
    if request.values:
        username = request.form["username"]
        password = request.form["password"]
        if validate_user(username, password):
            flash("Logged in successfully")
            response = make_response(
                redirect(url_for('dashboard')))
            session['username'] = username
            return response
        else:
            error = "Username/Password is wrong"
            flash(error)
            app.logger.warning("Failed user login by user "+username)
            return render_template("login.html")


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    session.pop('username', None)
    flash('You have logged out')
    return response


@app.route('/dashboard/')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template("dashboard.html", username=username)
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))


def validate_user(username, password):

    # DB
    MYSQL_DATABASE_HOST = os.getenv('IP', '0.0.0.0')
    MYSQL_DATABASE_USER = os.getenv('db_user', 'root')
    MYSQL_DATABASE_PASSWORD = os.getenv('db_password', 'root')
    MYSQL_DATABASE_NAME = os.getenv('db_name', 'flask_blog')

    conn = pymysql.Connect(
        host=MYSQL_DATABASE_HOST,
        user=MYSQL_DATABASE_USER,
        passwd=MYSQL_DATABASE_PASSWORD,
        db=MYSQL_DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users where username='%s' AND password='%s'" % (username, password))
    valid_user = cursor.fetchone()

    if valid_user:
        return True
    else:
        return False


if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', '5050'))
    app.debug = True
    app.secret_key = '-de\xd3Hb<\x96\x14\x8cy\x85e~n\x155ds6QId\xa6'

    # logging
    handlers = RotatingFileHandler(
        "writable/log/error.log", maxBytes=10000, backupCount=1)
    handlers.setLevel(logging.INFO)
    app.logger.addHandler(handlers)
    app.run(host=host, port=port)
