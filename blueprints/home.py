from flask import request, render_template, Blueprint
from Casino.helper_functions.user_administration import userid_from_token, userdata_from_id

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def homepage():
    if request.method == "GET":
        return render_template("home.html")