import os
from flask import Flask, url_for, request, render_template, redirect, flash

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
            return redirect(url_for('dashboard', username=username))
        else:
            error = "Username/Password is wrong"
            return render_template("login.html", error=error)


@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template("dashboard.html", username=username)


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
