from flask import Blueprint, request, render_template

from helper_functions.user_administration import userid_from_token, userdata_from_id, update_balance, played_game

account_blueprint = Blueprint('coinflip', __name__)


@account_blueprint.route('/', methods=["GET", "POST"])
def account():
    if request.method == "GET":
        # return account page (information, security etc.)
        return render_template("account.html")