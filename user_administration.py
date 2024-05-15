from mysqlClass import MySQL
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets

ph = PasswordHasher()


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
    token = secrets.token_urlsafe(64)
    with MySQL("INSERT") as curs:
        curs.execute('INSERT INTO sessions (token, user_id) VALUES (%s, ('
                     'SELECT id FROM users WHERE username=%s))',
                     (token, username))
    return token


def userid_from_token(token):
    with MySQL("SELECT") as curs:
        curs.execute("SELECT user_id, created_at FROM sessions WHERE token=%s;", (str(token),))
        x = curs.fetchall()
    if x is not None:
        return x[0][0]
    else:
        return None


def userdata_from_id(user_id):
    with MySQL("SELECT") as curs:
        curs.execute("SELECT username, balance FROM users WHERE id=%s;", (str(user_id), ))
        x = curs.fetchall()
    if x is not None:
        return {
            'username': x[0][0],
            'balance': x[0][1]
        }
    else:
        return None
