from flask import Flask, render_template, request
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets
import mysql.connector

app = Flask(__name__)
ph = PasswordHasher()

con = mysql.connector.connect(user='Betonblock', password='somepasswordformysql',
                              host='Betonblock.mysql.pythonanywhere-services.com',
                              database='Betonblock$casino')
cur = con.cursor()


def valid_login(username, password):
    cur.execute('SELECT password FROM users WHERE username=%s', (username,))
    hash = cur.fetchone()[0]
    try:
        return ph.verify(hash, password)
    except VerifyMismatchError:
        return False


def user_exists(username):
    cur.execute('SELECT 1 FROM users WHERE username=%s', (username,))
    return bool(len(cur.fetchall()))


def register_user(username, password):
    hash = ph.hash(password)
    cur.execute('INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)',
                (username, hash, 0))
    con.commit()


def create_token(username):
    token = secrets.token_urlsafe(64)
    cur.execute('INSERT INTO sessions (token, user_id) VALUES (%s, ('
                'SELECT id FROM users WHERE username=%s))',
                (token, username))
    con.commit()
    return token


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if valid_login(username, password):
            token = create_token(username)
            return "success " + token
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
            return "succes " + token

    elif request.method == "GET":
        return render_template("register.html")
