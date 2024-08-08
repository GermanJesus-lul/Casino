import random

from flask import Blueprint, request, render_template, jsonify

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game

minesweeper_blueprint = Blueprint('minesweeper', __name__)

mineField = [False] * 25
user_bet = 0
user_cash_out_val = 0
mines_count = 0
user_guesses_count = 0
game_running = False


@minesweeper_blueprint.route('/')
def minesweeper_home():
    if request.method == 'GET':
        return render_template("minesweeper/minesweeper.html")


@minesweeper_blueprint.route('/newGame', methods=["POST"])
def create_minesweeper():
    global user_bet
    if user_bet != 0:
        return "theres already a game running"
    content = request.json

    count = content["count"]
    bet = content["bet"]

    print("Count: " + str(count) + " Bet: " + str(bet))

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)

    if 25 > count > 0 and bet <= int(user_data['balance']):

        update_balance(user_id, bet * -1)  # subtracts bet value from user balance

        global user_cash_out_val, mines_count, user_guesses_count, mineField, game_running
        game_running = True
        user_bet = bet  # set value of global variable 'user_bet' to the bet amount
        user_cash_out_val = bet
        mines_count = count  # sets value of global 'mines_count' to the mines count
        mineField = [False] * 25  # fills a list with 25 elements with false value (no mine)
        user_guesses_count = 0  # resets user guess count to 0
        for i in range(count):  # fills minefield with picked number of mines
            r = random.randint(0, 24)
            if not mineField[r]:
                mineField[r] = True
            else:
                i -= 1
        return "minesweeper created"
    else:
        if count >= 25:
            return "to many mines"
        if count < 1:
            return "can't have less than 1 mine"
        else:
            return "not enough balance left"


@minesweeper_blueprint.route('/try', methods=["POST"])
def get_field_value():
    content = request.json

    pos = content["pos"]

    global user_cash_out_val, mines_count, user_guesses_count, mineField
    if mineField[pos]:
        user_cash_out_val = 0
        return jsonify(0, 0)
    else:
        multiplier = round((mines_count / (25 - user_guesses_count)) + 1, 2)
        user_guesses_count += 1
        user_cash_out_val = round(multiplier * user_cash_out_val, 2)
        return jsonify(multiplier, user_cash_out_val)


@minesweeper_blueprint.route('/cashOut', methods=["POST"])
def cash_out_minesweeper():
    global user_bet, user_cash_out_val, mineField

    user_id = userid_from_token(request.cookies.get('token'))

    update_balance(user_id, user_cash_out_val)

    ret_str = "Cashed out {:.2f}".format(user_cash_out_val)

    user_cash_out_val = 0
    user_bet = 0

    return ret_str
