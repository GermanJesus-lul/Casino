import random

from flask import Blueprint, request, render_template

from Casino.helper_functions.user_administration import userid_from_token, userdata_from_id, add_balance, remove_balance

coinflip_blueprint = Blueprint('coinflip', __name__)


@coinflip_blueprint.route('/')
def coinflip_home():
    if request.method == "GET":
        return render_template("coinflip.html")


@coinflip_blueprint.route('/flip', methods=["POST"])
def flip():
    content = request.json

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)

    if int(user_data['balance']) >= int(content['bet']):
        result = random.choice(["head", "tail"])
        if result == content["choice"]:
            add_balance(user_id, int(content['bet']))
            return "won"
        else:
            remove_balance(user_id, int(content['bet']))
            return "lost"
    else:
        return "not enough money"
