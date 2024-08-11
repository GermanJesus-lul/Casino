import random
import json

from flask import Blueprint, request, render_template, jsonify, session

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game

minesweeper_blueprint = Blueprint('minesweeper', __name__)


@minesweeper_blueprint.route('/', methods=["GET"])
def minesweeper_home():
    return render_template("minesweeper/minesweeper.html")


@minesweeper_blueprint.route('/newGame', methods=["POST"])
def create_minesweeper():
    game_data = session.get("minesweeper")
    if game_data:
        game = json.loads(game_data)
        if game["user_bet"] != 0:
            cash_out_minesweeper()
    else:
        game = {
            "user_bet": 0,
            "minefield": [False] * 25,
            "user_cash_out_val": 0,
            "mines_count": 0,
            "user_guesses_count": 0,
            "game_running": False
        }
    content = request.json

    count = content["count"]
    bet = content["bet"]

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)

    if 25 > count > 0 and 0 < bet <= int(user_data['balance']):

        update_balance(user_id, bet * -1)  # subtracts bet value from user balance

        game["game_running"] = True
        game["user_bet"] = bet
        game["user_cash_out_val"] = bet
        game["cash_out_minesweeper"] = bet
        game["mine_count"] = count
        game["minefield"] = [False] * 25
        game["user_guesses_count"] = 0
        for i in range(count):  # fills minefield with picked number of mines
            r = random.randint(0, 24)
            if not game["minefield"][r]:
                game["minefield"][r] = True
            else:
                i -= 1
        session["minesweeper"] = json.dumps(game)
        return "minesweeper created"
    else:
        if count >= 25:
            return "to many mines"
        if count < 1:
            return "can't have less than 1 mine"
        else:
            return "not enough balance left"


@minesweeper_blueprint.route('/try', methods=["POST"])
def try_minesweeper():
    content = request.json

    pos = content["pos"]

    game_data = session.get("minesweeper")
    if game_data:
        game = json.loads(game_data)
    else:
        return "No game running"

    if game["minefield"][pos]:
        game["user_cash_out_val"] = 0
        return jsonify(0, 0)
    else:
        game["multiplier"] = round((game["mines_count"] / (25 - game["user_guesses_count"])) + 1, 2)
        game["user_guesses_count"] += 1
        game["user_cash_out_val"] = round(game["multiplier"] * game["user_cash_out_val"], 2)
        return jsonify(game["multiplier"], game["user_cash_out_val"])


@minesweeper_blueprint.route('/cashOut', methods=["POST"])
def cash_out_minesweeper():
    game_data = session.get("minesweeper")
    if game_data:
        game = json.loads(game_data)
    else:
        return "No game running"

    user_id = userid_from_token(request.cookies.get('token'))

    update_balance(user_id, game["user_cash_out_val"])

    ret_str = "Cashed out {:.2f}".format(game["user_cash_out_val"])
    played_game(user_id, game["user_cash_out_val"] - game["user_bet"], "minesweeper", text_field=ret_str)

    user_cash_out_val = 0
    user_bet = 0

    return ret_str
