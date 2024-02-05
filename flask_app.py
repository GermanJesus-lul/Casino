from flask import Flask, render_template, request, make_response, redirect
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets
import mysql.connector

app = Flask(__name__)
ph = PasswordHasher()


class MySQL:
    def __init__(self, sql_type):
        self.sql_type = sql_type

    def __enter__(self):
        self.con = mysql.connector.connect(user='Betonblock', password='somepasswordformysql',
                                  host='Betonblock.mysql.pythonanywhere-services.com',
                                  database='Betonblock$casino')
        self.cur = self.con.cursor(buffered=True)
        return self.cur

    def __exit__(self, *args):
        if self.sql_type == "INSERT":
            self.con.commit()
        self.cur.close()
        self.con.close()


def valid_login(username, password):
    with MySQL("SELECT") as curs:
        curs.execute('SELECT password FROM users WHERE username=%s', (username,))
        phash = curs.fetchone()[0]
    try:
        return ph.verify(phash, password)
    except VerifyMismatchError:
        return False


def user_exists(username):
    with MySQL("SELECT") as curs:
        curs.execute('SELECT 1 FROM users WHERE username=%s', (username,))
        return bool(len(curs.fetchall()))


def register_user(username, password):
    phash = ph.hash(password)
    with MySQL("INSERT") as curs:
        curs.execute('INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)',
                    (username, phash, 0))


def create_token(username):
    token = secrets.token_urlsafe(2)
    with MySQL("INSERT") as curs:
        curs.execute('INSERT INTO sessions (token, user_id) VALUES (%s, ('
                    'SELECT id FROM users WHERE username=%s))',
                    (token, username))
    return token


def userid_from_token(token):
    with MySQL("SELECT") as curs:
        curs.execute("SELECT user_id, created_at FROM sessions WHERE token=%s;", (str(token), ))
        x = curs.fetchall()
    if x is not None:
        return x[0][0]
    else:
        return None


@app.route("/")
def home():
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
            return 'cookie not set'
        user_id = userid_from_token(token)
        if not user_id:
            return 'invalid token'
        return 'success ' + str(user_id)
