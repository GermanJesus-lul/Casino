import json
import random

from flask import Blueprint, request, render_template, jsonify, session

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game
from game_classes.black_jack.black_jack_game import BlackJackGame
from game_classes.black_jack.card import Card
from game_classes.black_jack.card_deck import CardDeck
from game_classes.black_jack.dealer import Dealer
from game_classes.black_jack.player import Player


black_jack_blueprint = Blueprint('black_jack', __name__)


@black_jack_blueprint.route('/start', methods=["POST"])
def start():
    try:
        content = request.json
        user_id = userid_from_token(request.cookies.get('token'))
        user_data = userdata_from_id(user_id)
        bet_amount = int(content['bet'])

        if bet_amount < 1:
            return jsonify({"message": "Bet amount must be greater than 0."}), 400

        if user_data['balance'] >= bet_amount:
            game = BlackJackGame()
            game.deck.build_deck()
            game.deck.shuffle_deck()
            start_response = game.start_game()
            save_current_game(game)
            session['bet_amount'] = bet_amount
            return jsonify(start_response)
        else:
            return jsonify({"message": "You can't bet more money than you have!"}), 400
    except Exception as e:
        print(f"Error during start: {e}")
        return jsonify({"message": "An error occurred while starting the game."}), 500


@black_jack_blueprint.route('/')
def black_jack_home():
    if request.method == "GET":
        return render_template("black_jack/black_jack.html")


@black_jack_blueprint.route('/hit', methods=["POST"])
def hit():
    try:
        game = get_current_game()
        if game is None:
            return jsonify({"message": "No game in progress."}), 400
        hit_result = game.hit()
        save_current_game(game)
        return jsonify(hit_result)
    except Exception as e:
        return jsonify({"message": "An error occurred while hitting."}), 500


@black_jack_blueprint.route('/stay', methods=["POST"])
def stay():
    try:
        game = get_current_game()
        if game is None:
            return jsonify({"message": "No game in progress."}), 400
        stay_result = game.stay()
        save_current_game(game)
        return jsonify(stay_result)
    except Exception as e:
        return jsonify({"message": "An error occurred while staying."}), 500


@black_jack_blueprint.route('/restart', methods=["POST"])
def restart():
    try:
        game = get_current_game()
        restart_result = game.restart()
        save_current_game(game)
        return jsonify(restart_result)
    except Exception as e:
        return jsonify({"message": "An error occurred while restarting."}), 500


@black_jack_blueprint.route('/get_game_state', methods=["GET"])
def get_game():
    game = get_current_game()
    return jsonify(game.get_game_state())


def get_current_game():
    game_data = session.get('blackjack_game')
    if game_data:
        return BlackJackGame.from_dict(json.loads(game_data))
    return None


def save_current_game(game):
    game_data = game.to_dict()
    session['blackjack_game'] = json.dumps(game_data)
