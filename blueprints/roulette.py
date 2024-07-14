import random

from flask import Blueprint, request, render_template

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game

roulette_blueprint = Blueprint('roulette', __name__)

red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 29, 31, 33, 35]
green = [0]

even = [i for i in range(0, 37) if i % 2 == 0]
odd = [i for i in range(0, 37) if i % 2 != 0]


@roulette_blueprint.route('/')
def roulette_home():
    if request.method == "GET":
        return render_template("roulette/roulette.html")


@roulette_blueprint.route('/spin', methods=["POST"])
def spin():
    content = request.json

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)

    if int(user_data['balance']) >= int(content['bet']):
        result = random.randint(0, 37)
        if content['type'] == "number":
            if int(content['number']) is None:
                return "invalid number"
            elif int(content['number']) == result:
                bet_value = 36 * int(content['bet'])
            else:
                bet_value = -int(content['bet'])
        elif content['choice'] is None:
            return "invalid choice"
        elif content['type'] == "evenodd":
            if content['choice'] == "even" and result in even or content['choice'] == "odd" and result in odd:
                bet_value = int(content['bet'])
            else:
                bet_value = -int(content['bet'])
        elif content['type'] == "color":
            if content['choice'] == "red" and result in red or content['choice'] == "black" and result in black:
                bet_value = int(content['bet'])
            else:
                bet_value = -int(content['bet'])
        else:
            return "invalid choice"

        update_balance(user_id, bet_value)
        played_game(user_id, bet_value, "roulette", double_field=result)

        return str(result)
    else:
        return "not enough money"
