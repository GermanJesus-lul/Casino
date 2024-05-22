import random

from flask import Blueprint, request, render_template, redirect, url_for

from Casino.helper_functions.user_administration import userid_from_token, userdata_from_id

coinflip_blueprint = Blueprint('coinflip', __name__)


@coinflip_blueprint.route('/')
def coinflip_home():
    if request.method == "GET":
        user_id = userid_from_token(request.cookies.get('token'))
        user_data = userdata_from_id(user_id)
        # return home page with info
        return render_template("coinflip.html",
                               username=user_data['username'],
                               balance=user_data['balance'])


@coinflip_blueprint.route('/flip')
def flip():
    ishead = random.getrandbits(1)
    return ishead
