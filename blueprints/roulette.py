import random

from flask import Blueprint, request, render_template

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game

roulette_blueprint = Blueprint('roulette', __name__)


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
            even = content['choice'] == "even" and result % 2 == 0
            odd = content['choice'] == "odd" and result % 2 == 1
            if (even or odd) and result != 0:
                bet_value = int(content['bet'])
            else:
                bet_value = -int(content['bet'])
        elif content['type'] == "color":
            red = [1, 2, 3, 4, 5, 7, 9, 12, 14, 15, 16, 17, 18, 23, 27, 30, 36, 37]
            black = [6, 8, 10, 11, 13, 19, 20, 21, 22, 24, 25, 26, 28, 29, 31, 32, 33, 34, 35]
            b_red = content['choice'] == "red" and result in red
            b_black = content['choice'] == "black" and result in black
            if b_red or b_black:
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
