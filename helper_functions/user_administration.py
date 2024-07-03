from helper_functions.sqlClass import SQL
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets

ph = PasswordHasher()


def valid_login(username, password):
    with SQL("SELECT") as curs:
        curs.execute(f'SELECT password FROM users WHERE username="{username}"')
        phash = curs.fetchone()[0]
    try:
        return ph.verify(phash, password)
    except VerifyMismatchError:
        return False


def user_exists(username):
    with SQL("SELECT") as curs:
        curs.execute(f'SELECT 1 FROM users WHERE username="{username}"')
        return bool(len(curs.fetchall()))


def register_user(username, password):
    phash = ph.hash(password)
    with SQL("INSERT") as curs:
        curs.execute(f'INSERT INTO users (username, password, balance) VALUES ("{username}", "{phash}", 100)')


def create_token(username):
    token = secrets.token_urlsafe(64)
    with SQL("INSERT") as curs:
        curs.execute(f'INSERT INTO sessions (token, user_id) VALUES ("{token}", ('
                     f'SELECT id FROM users WHERE username="{username}"))')
    return token


def userid_from_token(token):
    with SQL("SELECT") as curs:
        curs.execute(f'SELECT user_id, created_at FROM sessions WHERE token="{str(token)}"')
        x = curs.fetchall()
    if x is not None and len(x) > 0:
        return x[0][0]
    else:
        return None


def userdata_from_id(user_id):
    with SQL("SELECT") as curs:
        curs.execute(f"SELECT username, balance FROM users WHERE id={str(user_id)}")
        x = curs.fetchall()
    if x is not None and len(x) > 0:
        return {
            'username': x[0][0],
            'balance': x[0][1]
        }
    else:
        return None


def update_balance(user_id, amount):
    with SQL("UPDATE") as curs:
        curs.execute(f'UPDATE users SET balance = balance + {amount} WHERE id={user_id}')


def played_game(user_id, balance, game_name, double_field=None, text_field=None):
    # get game_id
    with SQL("SELECT") as curs:
        curs.execute(f'SELECT id FROM games WHERE name="{game_name}"')
        game_id = curs.fetchone()[0]
    # update game stats
    with SQL("UPDATE") as curs:
        curs.execute(f'UPDATE games SET total_value = total_value + {balance}, games_played = games_played + 1 WHERE id={game_id}')
    # add history item
    with SQL("INSERT") as curs:
        if double_field is not None and text_field is not None:
            curs.execute(f'INSERT INTO history (user_id, value, game_id, field_1, field_2)'
                         f' VALUES ({user_id}, {balance}, {game_id}, {double_field}, "{text_field}")')
        elif double_field is not None:
            curs.execute(f'INSERT INTO history (user_id, value, game_id, field_1)'
                         f' VALUES ({user_id}, {balance}, {game_id}, {double_field})')
        elif text_field is not None:
            curs.execute(f'INSERT INTO history (user_id, value, game_id, field_2)'
                         f' VALUES ({user_id}, {balance}, {game_id}, "{text_field}")')
        else:
            curs.execute(f'INSERT INTO history (user_id, value, game_id)'
                         f' VALUES ({user_id}, {balance}, {game_id})')