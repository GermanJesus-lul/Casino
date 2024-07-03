import random

from flask import Blueprint, request, render_template

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance, played_game

roulette_blueprint = Blueprint('roulette', __name__)

red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 29, 31, 33, 35]
green = [0]


@roulette_blueprint.route('/')
def roulette_home():
    if request.method == "GET":
        return render_template("roulette.html")


@roulette_blueprint.route('/spin', methods=["POST"])
def spin():
    content = request.json

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)

    if int(user_data['balance']) >= int(content['bet']):
        result = random.randint(0, 37)
        if content['choice'] == "red" and result in red or content['choice'] == "black" and result in black or \
                content['choice'] == "green" and result in green:
            bet_value = int(content['bet'])
        else:
            bet_value = -int(content['bet'])

        update_balance(user_id, bet_value)
        played_game(user_id, bet_value, "roulette", text_field=str(result))

        return str(result)
    else:
        return "not enough money"
