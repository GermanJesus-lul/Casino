from flask import Blueprint, request, render_template

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance
from helper_functions.stats import played_game

minesweeper_blueprint = Blueprint('minesweeper', __name__)

@minesweeper_blueprint.route('/')
def minesweeper_home():
    if request.method == 'GET':
        return render_template("minesweeper/minesweeper.html")
