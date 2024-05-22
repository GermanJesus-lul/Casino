from flask import request, render_template, Blueprint
from Casino.helper_functions.user_administration import userid_from_token, userdata_from_id

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def homepage():
    if request.method == "GET":
        user_id = userid_from_token(request.cookies.get('token'))
        user_data = userdata_from_id(user_id)
        # return home page with info
        return render_template("home.html",
                               username=userdata_from_id(user_id)['username'],
                               balance=userdata_from_id(user_id)['balance'])