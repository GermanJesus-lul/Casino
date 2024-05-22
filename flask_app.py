from flask import Flask, render_template, request, make_response, redirect
import git

from Casino.user_administration import *

app = Flask(__name__)


@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/Betonblock/Casino')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route("/")
def home():
    if request.method == "GET":
        token = request.cookies.get('token')
        if not token:
            return redirect('/login')
        user_id = userid_from_token(token)
        if not user_id:
            return redirect('/login')
        # return home page with info
        return render_template("home.html",
                               username=userdata_from_id(user_id)['username'],
                               balance=userdata_from_id(user_id)['balance'])
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
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


@app.route("/register", methods=["GET", "POST"])
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


@app.route('/account', methods=["GET", "POST"])
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
