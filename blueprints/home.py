from flask import request, redirect, render_template, Blueprint
from Casino.helper_functions.user_administration import userid_from_token, userdata_from_id

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def homepage():
    if request.method == "GET":
        token = request.cookies.get('token')
        if not token:
            return redirect('/login')
        user_id = userid_from_token(token)
        if not user_id:
            return redirect('/login')
        # return home page with info
        return render_template("home.html",
                               username=userdata_from_id(user_id)['username'],
                               balance=userdata_from_id(user_id)['balance'])
    return render_template("home.html")