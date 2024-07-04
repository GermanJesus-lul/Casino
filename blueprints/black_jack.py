import random

from flask import Blueprint, request, render_template, jsonify

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance, played_game

black_jack_blueprint = Blueprint('black_jack', __name__)


deck = []
values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
types = ['clubs', 'diamonds', 'hearts', 'spades']


def build_deck():
    global deck
    deck = [f"{t}_{v}" for t in types for v in values]
    random.shuffle(deck)


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


@black_jack_blueprint.route('/deal', methods=["POST"])
def deal():
    build_deck()
    player_cards = [deck.pop(), deck.pop()]
    dealer_cards = [deck.pop(), deck.pop()]
    player_sum = sum(get_value(card) for card in player_cards)
    dealer_sum = sum(get_value(card) for card in dealer_cards)
    player_ace_count = sum(check_ace(card) for card in player_cards)
    dealer_ace_count = sum(check_ace(card) for card in dealer_cards)
    player_sum = reduce_ace(player_sum, player_ace_count)
    dealer_sum = reduce_ace(dealer_sum, dealer_ace_count)
    response = {
        "player_cards": player_cards,
        "dealer_cards": [dealer_cards[0],"back"],
        "player_sum": player_sum,
        "dealer_sum": get_value(dealer_cards[0]),
        "player_ace_count": player_ace_count,
        "dealer_ace_count": dealer_ace_count
    }
    return jsonify(response)


@black_jack_blueprint.route('/hit', methods=["POST"])
def hit():
    card = deck.pop()
    card_value = get_value(card)
    card_ace = check_ace(card)
    return jsonify({"card": card, "value": card_value, "ace": card_ace})


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
