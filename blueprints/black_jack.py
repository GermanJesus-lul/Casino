import json
import random

from flask import Blueprint, request, render_template, jsonify, session

from helper_functions.user_administration import userid_from_token, userdata_from_id

black_jack_blueprint = Blueprint('black_jack', __name__)


@black_jack_blueprint.route('/start', methods=["GET"])
def start():
    game = BlackJack()
    game.build_deck()
    game.shuffle_deck()
    start_response = game.start_game()
    save_current_game(game)
    return jsonify(start_response)


@black_jack_blueprint.route('/')
def black_jack_home():
    if request.method == "GET":
        return render_template("black_jack/black_jack.html")


@black_jack_blueprint.route('/play', methods=["POST"])
def play():
    content = request.json

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)


@black_jack_blueprint.route('/hit', methods=["GET"])
def hit():
    game = get_current_game()
    hit_result = game.hit()
    save_current_game(game)
    return jsonify(hit_result)


@black_jack_blueprint.route('/stay', methods=["GET"])
def stay():
    game = get_current_game()
    stay_result = game.stay()
    return jsonify(stay_result)


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
        self.canHit = True
        self.cardsDealer = []
        self.cardsPlayer = []
        self.canStart = True

    def to_dict(self):
        return {
            "dealerSum": self.dealerSum,
            "playerSum": self.playerSum,
            "dealerAceCount": self.dealerAceCount,
            "playerAceCount": self.playerAceCount,
            "hiddenCard": self.hiddenCard,
            "deck": self.deck,
            "canHit": self.canHit,
            "cardsDealer": self.cardsDealer,
            "cardsPlayer": self.cardsPlayer,
            "canStart": self.canStart
        }

    def from_dict(self, data):
        self.dealerSum = data['dealerSum']
        self.playerSum = data['playerSum']
        self.dealerAceCount = data['dealerAceCount']
        self.playerAceCount = data['playerAceCount']
        self.hiddenCard = data['hiddenCard']
        self.deck = data['deck']
        self.canHit = data['canHit']
        self.cardsDealer = data['cardsDealer']
        self.cardsPlayer = data['cardsPlayer']
        self.canStart = data['canStart']

    def build_deck(self):
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        types = ['clubs', 'diamonds', 'hearts', 'spades']
        self.deck = [f"{t}_{v}" for t in types for v in values]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def start_game(self):
        print("start game")
        self.hiddenCard = self.deck.pop()
        self.dealerSum += self.get_value(self.hiddenCard)
        self.dealerAceCount += self.check_ace(self.hiddenCard)
        print(f"dealer initial hidden card: {self.hiddenCard}, dealer sum: {self.dealerSum}, dealer ace count: {self.dealerAceCount}")
        while self.dealerSum < 17:
            card = self.deck.pop()
            self.dealerSum += self.get_value(card)
            self.dealerAceCount += self.check_ace(card)
            self.dealerSum, self.dealerAceCount = self.reduce_ace(self.dealerSum, self.dealerAceCount)
            self.cardsDealer.append(card)
            print(f"Dealer draws: {card}, Dealer Sum: {self.dealerSum}")
        for i in range(2):
            card = self.deck.pop()
            self.playerSum += self.get_value(card)
            self.playerAceCount += self.check_ace(card)
            self.playerSum, self.playerAceCount = self.reduce_ace(self.playerSum, self.playerAceCount)
            self.cardsPlayer.append(card)
            print(f"Player draws: {card}, Player Sum: {self.playerSum}")
        return {"message": "start", "dealerSum": self.dealerSum, "playerSum": self.playerSum, "hiddenCard": self.hiddenCard,"canHit": self.canHit, "cardsDealer": self.cardsDealer, "cardsPlayer": self.cardsPlayer}

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
        message = "hit"
        if self.canHit:
            print("Player hits...")
            card = self.deck.pop()
            self.playerSum += self.get_value(card)
            self.playerAceCount += self.check_ace(card)
            self.playerSum, self.playerAceCount = self.reduce_ace(self.playerSum, self.playerAceCount)
            self.cardsPlayer.append(card)
            print(f"Player draws: {card}, Player Sum: {self.playerSum}")
            if self.playerSum > 21:
                self.canHit = False
                message = "Player busts!"
                print("Player busts!")

        return {"message": message, "dealerSum": self.dealerSum, "playerSum": self.playerSum, "hiddenCard": self.hiddenCard,"canHit": self.canHit, "cardsDealer": self.cardsDealer, "cardsPlayer": self.cardsPlayer}

    def stay(self):
        self.canHit = False
        print(f"Player stays. Final Player Sum: {self.playerSum}, Dealer Sum: {self.dealerSum}")
        if self.playerSum > 21:
            message = "Player busts!"
        elif self.dealerSum > 21:
            message = "Dealer busts!"
        elif self.playerSum > self.dealerSum:
            message = "Player wins!"
        elif self.playerSum < self.dealerSum:
            message = "Dealer wins!"
        else:
            message = "Tie!"
        return {"message": message, "dealerSum": self.dealerSum, "playerSum": self.playerSum, "hiddenCard": self.hiddenCard,"canHit": self.canHit, "cardsDealer": self.cardsDealer, "cardsPlayer": self.cardsPlayer}
