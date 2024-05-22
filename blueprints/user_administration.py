from flask import request, redirect, render_template, make_response, Blueprint
from Casino.helper_functions.user_administration import *

user_administration_blueprint = Blueprint('user_administration', __name__)


@user_administration_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_exists(username):
            if valid_login(username, password):
                token = create_token(username)
                resp = make_response(redirect('/account'))
                resp.set_cookie('token', token)
                return resp
        return "failed"

    elif request.method == "GET":
        return render_template("login.html")


@user_administration_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_exists(username):
            return "user already exists"
        else:
            register_user(username, password)
            token = create_token(username)
            resp = make_response(redirect('/account'))
            resp.set_cookie('token', token)
            return resp

    elif request.method == "GET":
        return render_template("register.html")


@user_administration_blueprint.route('/account', methods=["GET", "POST"])
def account():
    if request.method == "GET":
        token = request.cookies.get('token')
        if not token:
            return redirect('/login')
        user_id = userid_from_token(token)
        if not user_id:
            return redirect('/login')
        # return account page (information, security etc.)
        return 'success ' + str(user_id)