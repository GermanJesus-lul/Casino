from flask import request, render_template, Blueprint

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def homepage():
    if request.method == "GET":
        return render_template("home.html")