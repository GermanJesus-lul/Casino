from flask import Blueprint, request, render_template

from helper_functions.user_administration import userid_from_token
from helper_functions.stats import get_history_stats

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/account', methods=["GET", "POST"])
def account():
    if request.method == "GET":
        # return account page (information, security etc.)
        return render_template("account.html")


@account_blueprint.route("/stats", methods=["GET"])
def stats():
    user_id = userid_from_token(request.cookies.get('token'))
    return get_history_stats(user_id)
