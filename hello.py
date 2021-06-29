import os
from flask import Flask, url_for, request, render_template, redirect, flash
from flask.helpers import make_response
from werkzeug.wrappers import response

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
            response.set_cookie('username', username)
            return response
        else:
            error = "Username/Password is wrong"
            return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('username', '', 0)
    flash('You have logged out')
    return response


@app.route('/dashboard/')
def dashboard():
    username = request.cookies.get('username')
    if username:
        return render_template("dashboard.html", username=username)
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))


def validate_user(username, password):
    if username == password:
        return True
    else:
        return False


if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', '5050'))
    app.debug = True
    app.secret_key = 'superKey'
    app.run(host=host, port=port)
