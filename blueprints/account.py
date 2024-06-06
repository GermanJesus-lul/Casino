from flask import Blueprint, request, render_template

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/account', methods=["GET", "POST"])
def account():
    if request.method == "GET":
        # return account page (information, security etc.)
        return render_template("account.html")