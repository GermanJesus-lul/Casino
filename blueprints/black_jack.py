import random

from flask import Blueprint, request, render_template, jsonify

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance, played_game

black_jack_blueprint = Blueprint('black_jack', __name__)


@black_jack_blueprint.route('/start', methods=["GET"])
def start():
    build_deck()
    shuffle_deck()
    start_game()
    return jsonify({"message": "Game started", "dealerSum": dealerSum, "playerSum": playerSum, "hiddenCard": hiddenCard, "canHit": canHit, "cardsDealer": cardsDealer, "cardsPlayer": cardsPlayer})


dealerSum = 0
playerSum = 0
dealerAceCount = 0
playerAceCount = 0
hiddenCard = ""
deck = []
canHit = True
cardsDealer = []
cardsPlayer = []
canStart = True

def build_deck():
    global deck
    values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
    types = ['clubs', 'diamonds', 'hearts', 'spades']
    deck = [f"{t}_{v}" for t in types for v in values]


def shuffle_deck():
    global deck
    random.shuffle(deck)


def start_game():
    global hiddenCard, dealerSum, dealerAceCount, cardsDealer, playerSum, playerAceCount, cardsPlayer
    hiddenCard = deck.pop()
    dealerSum += get_value(hiddenCard)
    dealerAceCount += check_ace(hiddenCard)
    while dealerSum < 17:
        card = deck.pop()
        dealerSum += get_value(card)
        dealerAceCount += check_ace(card)
        dealerSum = reduce_ace(dealerSum, dealerAceCount)
        cardsDealer.append(card)
    for i in range(2):
        card = deck.pop()
        playerSum += get_value(card)
        playerAceCount += check_ace(card)
        playerSum = reduce_ace(playerSum, playerAceCount)
        cardsPlayer.append(card)


def get_value(card):
    value = card.split('_')[1]
    if value == 'ace':
        return 11
    elif value in ['jack', 'queen', 'king']:
        return 10
    else:
        return int(value)


def check_ace(card):
    return 1 if card.split('_')[1] == 'ace' else 0


def reduce_ace(player_sum, player_ace_count):
    while player_sum > 21 and player_ace_count > 0:
        player_sum -= 10
        player_ace_count -= 1
    return player_sum


@black_jack_blueprint.route('/')
def black_jack_home():
    if request.method == "GET":
        return render_template("black_jack.html")


@black_jack_blueprint.route('/play', methods=["POST"])
def play():
    content = request.json

    user_id = userid_from_token(request.cookies.get('token'))
    user_data = userdata_from_id(user_id)


@black_jack_blueprint.route('/hit', methods=["POST"])
def hit():
    global playerSum, playerAceCount, canHit, cardsPlayer
    if canHit:
        card = deck.pop()
        playerSum += get_value(card)
        playerAceCount += check_ace(card)
        playerSum = reduce_ace(playerSum, playerAceCount)
        cardsPlayer.append(card)
        if playerSum > 21:
            canHit = False
    return jsonify({"message": "hit", "dealerSum": dealerSum, "playerSum": playerSum, "hiddenCard": hiddenCard, "canHit": canHit, "cardsDealer": cardsDealer, "cardsPlayer": cardsPlayer})


@black_jack_blueprint.route('/stay', methods=["POST"])
def stay():
    data = request.json
    dealer_sum = data['dealer_sum']
    dealer_ace_count = data['dealer_ace_count']
    dealer_cards = data['dealer_cards']

    while dealer_sum < 17:
        card = deck.pop()
        dealer_sum += get_value(card)
        dealer_ace_count += check_ace(card)
        dealer_sum = reduce_ace(dealer_sum, dealer_ace_count)
        dealer_cards.append(card)

    return jsonify({"dealer_sum": dealer_sum, "dealer_cards": dealer_cards})
