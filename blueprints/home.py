from flask import request, render_template, Blueprint
from Casino.helper_functions.user_administration import userid_from_token, userdata_from_id

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def homepage():
    if request.method == "GET":
        token = request.cookies.get('token')
        if token:
            user_id = userid_from_token(token)
            if user_id:
                user_data = userdata_from_id(user_id)
                # return home page with info
                return render_template("home.html",
                                       username=user_data['username'],
                                       balance=user_data['balance'])
        return render_template("home.html")