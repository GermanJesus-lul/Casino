from flask import session


def get_bet_amount():
    return session.get('bet_amount', 0)
