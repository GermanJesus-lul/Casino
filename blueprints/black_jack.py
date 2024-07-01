import random

from flask import Blueprint, request, render_template

from flask import jsonify

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance, played_game

black_jack_blueprint = Blueprint('black_jack', __name__)

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
    # This function will handle the initial dealing of cards
    # Generate two random cards for the dealer and the player
    # Remember to check if the cards are aces
    # Return the cards as a response
    pass  # Placeholder code

@black_jack_blueprint.route('/hit', methods=["POST"])
def hit():
    # This function will handle the player's hit action
    # Generate a random card
    # Check if the card is an ace
    # Add the card to the player's hand
    # Calculate the player's new sum
    # Check if the player has busted
    # Return the new card and the player's new sum as a response
    pass  # Placeholder code
@black_jack_blueprint.route('/stay', methods=["POST"])
def stay():
    # This function will handle the player's stay action
    # The dealer should continue to draw cards until their sum is 17 or higher
    # Determine the winner of the game
    # Update the player's balance based on the game result
    # Return the result of the game as a response
    pass  # Placeholder code