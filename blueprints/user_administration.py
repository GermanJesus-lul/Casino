from flask import request, redirect, render_template, make_response, Blueprint
from helper_functions.user_administration import *

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
        return render_template("errorpage.html", error="Log in failed", redirect="/login")

    elif request.method == "GET":
        return render_template("login.html")


@user_administration_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_exists(username):
            return render_template("errorpage.html", error="Username already exists", redirect="/register")
        else:
            register_user(username, password)
            token = create_token(username)
            resp = make_response(redirect('/account'))
            resp.set_cookie('token', token)
            return resp

    elif request.method == "GET":
        return render_template("register.html")


@user_administration_blueprint.route("/logout", methods=["GET"])
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('token', path='/', domain='casino.juliusgic.com')
    return resp


@user_administration_blueprint.route("/userdata", methods=["GET"])
def userdata():
    user_id = userid_from_token(request.cookies.get('token'))
    return userdata_from_id(user_id)
