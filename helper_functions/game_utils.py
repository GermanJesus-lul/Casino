from flask import session


# Function to retrieve the bet amount from the session
def get_bet_amount():
    return session.get('bet_amount', 0)
