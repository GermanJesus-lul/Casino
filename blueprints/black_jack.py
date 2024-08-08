import json
import random

from flask import Blueprint, request, render_template, jsonify, session

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game

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
            game = BlackJack()
            game.build_deck()
            game.shuffle_deck()
            start_response = game.start_game()
            save_current_game(game)
            session['bet_amount'] = bet_amount
            return jsonify(start_response)
        else:
            return jsonify({"message": "You can't bet more money than you have!"}), 400
    except Exception as e:
        print("Error during start: {e}")
        return jsonify({"message": "An error occurred while starting the game."}), 500


def get_bet_amount():
    return session.get('bet_amount', 0)


@black_jack_blueprint.route('/')
def black_jack_home():
    if request.method == "GET":
        return render_template("black_jack/black_jack.html")


@black_jack_blueprint.route('/hit', methods=["GET"])
def hit():
    try:
        game = get_current_game()
        hit_result = game.hit()
        save_current_game(game)
        return jsonify(hit_result)
    except Exception as e:
        print(f"Error during hit: {e}")
        return jsonify({"message": "An error occurred while hitting."}), 500


@black_jack_blueprint.route('/stay', methods=["GET"])
def stay():
    try:
        game = get_current_game()
        stay_result = game.stay()
        save_current_game(game)
        return jsonify(stay_result)
    except Exception as e:
        print(f"Error during stay: {e}")
        return jsonify({"message": "An error occurred while staying."}), 500


@black_jack_blueprint.route('/restart', methods=["GET"])
def restart():
    try:
        game = get_current_game()
        restart_result = game.restart()
        save_current_game(game)
        return jsonify(restart_result)
    except Exception as e:
        print(f"Error during restart: {e}")
        return jsonify({"message": "An error occurred while restarting."}), 500


@black_jack_blueprint.route('/get_game_state', methods=["GET"])
def get_game():
    game = get_current_game()
    return jsonify(game.get_game_state())


def get_current_game():
    if 'game' in session:
        game_data = json.loads(session['game'])
        game = BlackJack()
        game.from_dict(game_data)
        return game
    else:
        return None


def save_current_game(game):
    session['game'] = json.dumps(game.to_dict())


class BlackJack:
    def __init__(self):
        self.dealerSum = 0
        self.playerSum = 0
        self.dealerAceCount = 0
        self.playerAceCount = 0
        self.hiddenCard = ""
        self.deck = []
        self.cardsDealer = []
        self.cardsPlayer = []
        self.state = 'initial'  # Possible states: 'initial', 'playing', 'gameOver'

    def to_dict(self):
        return {
            "dealerSum": self.dealerSum,
            "playerSum": self.playerSum,
            "dealerAceCount": self.dealerAceCount,
            "playerAceCount": self.playerAceCount,
            "hiddenCard": self.hiddenCard,
            "deck": self.deck,
            "cardsDealer": self.cardsDealer,
            "cardsPlayer": self.cardsPlayer,
            "state": self.state
        }

    def from_dict(self, data):
        self.dealerSum = data['dealerSum']
        self.playerSum = data['playerSum']
        self.dealerAceCount = data['dealerAceCount']
        self.playerAceCount = data['playerAceCount']
        self.hiddenCard = data['hiddenCard']
        self.deck = data['deck']
        self.cardsDealer = data['cardsDealer']
        self.cardsPlayer = data['cardsPlayer']
        self.state = data['state']

    def build_deck(self):
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        types = ['clubs', 'diamonds', 'hearts', 'spades']
        self.deck = [f"{t}_{v}" for t in types for v in values]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def start_game(self):
        self.state = 'playing'
        self.hiddenCard = self.deck.pop()
        self.dealerSum += self.get_value(self.hiddenCard)
        self.dealerAceCount += self.check_ace(self.hiddenCard)
        while self.dealerSum < 17:
            card = self.deck.pop()
            self.dealerSum += self.get_value(card)
            self.dealerAceCount += self.check_ace(card)
            self.dealerSum, self.dealerAceCount = self.reduce_ace(self.dealerSum, self.dealerAceCount)
            self.cardsDealer.append(card)
        for i in range(2):
            card = self.deck.pop()
            self.playerSum += self.get_value(card)
            self.playerAceCount += self.check_ace(card)
            self.playerSum, self.playerAceCount = self.reduce_ace(self.playerSum, self.playerAceCount)
            self.cardsPlayer.append(card)
        return self.get_game_state()

    def get_value(self, card):
        value = card.split('_')[1]
        if value == 'ace':
            return 11
        elif value in ['jack', 'queen', 'king']:
            return 10
        else:
            return int(value)

    def check_ace(self, card):
        return 1 if card.split('_')[1] == 'ace' else 0

    def reduce_ace(self, sum, ace_count):
        while sum > 21 and ace_count > 0:
            sum -= 10
            ace_count -= 1
        return sum, ace_count

    def hit(self):
        if self.state != 'playing':
            return self.get_game_state()
        card = self.deck.pop()
        self.playerSum += self.get_value(card)
        self.playerAceCount += self.check_ace(card)
        self.playerSum, self.playerAceCount = self.reduce_ace(self.playerSum, self.playerAceCount)
        self.cardsPlayer.append(card)
        if self.playerSum > 21:
            self.state = 'gameOver'
            self.record_game_outcome("Player busts!", -get_bet_amount())
        return self.get_game_state()

    def stay(self):
        if self.state != 'playing':
            return self.get_game_state()
        self.state = 'gameOver'
        self.resolve_game()
        return self.get_game_state()

    def restart(self):
        self.dealerSum = 0
        self.playerSum = 0
        self.dealerAceCount = 0
        self.playerAceCount = 0
        self.hiddenCard = ""
        self.deck = []
        self.cardsDealer = []
        self.cardsPlayer = []
        self.state = 'initial'
        self.build_deck()
        self.shuffle_deck()
        return self.get_game_state()

    def resolve_game(self):
        user_id = userid_from_token(request.cookies.get('token'))
        bet_amount = get_bet_amount()
        if self.playerSum > 21:
            self.record_game_outcome("Player busts!", -bet_amount)
        elif self.dealerSum > 21:
            self.record_game_outcome("Dealer busts!", bet_amount)
        elif self.playerSum > self.dealerSum:
            self.record_game_outcome("Player wins!", bet_amount)
        elif self.playerSum < self.dealerSum:
            self.record_game_outcome("Dealer wins!", -bet_amount)
        else:
            self.record_game_outcome("Tie!", 0)

    def record_game_outcome(self, message, amount):
        user_id = userid_from_token(request.cookies.get('token'))
        update_balance(user_id, amount)
        played_game(user_id, amount, "blackjack", text_field=message)

    def get_game_state(self):
        game_state = {
            "state": self.state,
            "playerSum": self.playerSum,
            "cardsDealer": self.cardsDealer,
            "cardsPlayer": self.cardsPlayer,
            "message": self.get_message()
        }
        if self.state == 'gameOver':
            game_state['dealerSum'] = self.dealerSum
            game_state['hiddenCard'] = self.hiddenCard
        else:
            game_state['dealerSum'] = '?'
            game_state['hiddenCard'] = 'back'

        return game_state

    def get_message(self):
        if self.state == 'gameOver':
            if self.playerSum > 21:
                return "Player busts!"
            elif self.dealerSum > 21:
                return "Dealer busts!"
            elif self.playerSum > self.dealerSum:
                return "Player wins!"
            elif self.playerSum < self.dealerSum:
                return "Dealer wins!"
            else:
                return "Tie!"
        return ""
