import random

from flask import Blueprint, request, render_template

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game

coinflip_blueprint = Blueprint('coinflip', __name__)


@coinflip_blueprint.route('/')
def coinflip_home():
    if request.method == "GET":
        return render_template("coinflip/coinflip.html")


@coinflip_blueprint.route('/flip', methods=["POST"])
def flip():
    content = request.json

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)

    if int(user_data['balance']) >= int(content['bet']):
        result = random.choice(["head", "tail"])
        if result == content["choice"]:
            bet_value = int(content['bet'])
        else:
            bet_value = -int(content['bet'])

        update_balance(user_id, bet_value)
        played_game(user_id, bet_value, "coinflip", text_field=result)

        if bet_value > 0:
            return "won"
        else:
            return "lost"
    else:
        return "not enough money"
