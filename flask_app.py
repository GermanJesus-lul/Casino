from flask import Flask, request, redirect, url_for

from helper_functions.user_administration import userid_from_token

from blueprints.autodeployment import autodeployment_blueprint
from blueprints.home import home_blueprint
from blueprints.user_administration import user_administration_blueprint
from blueprints.coinflip import coinflip_blueprint
from blueprints.account import account_blueprint
from blueprints.roulette import roulette_blueprint

import config

app = Flask(__name__)
app.register_blueprint(autodeployment_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(user_administration_blueprint)
app.register_blueprint(account_blueprint)

# games
app.register_blueprint(coinflip_blueprint, url_prefix='/coinflip')
app.register_blueprint(roulette_blueprint, url_prefix='/roulette')

@app.before_request
def before_request():
    # force https
    if not request.is_secure and not config.local():
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

    # redirect to login if required
    login_required = True
    if str(request.url_rule) in ['/login', '/register', "/", '/update_server']:
        login_required = False
    if str(request.url_rule).startswith('/static'):
        login_required = False

    if login_required:
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('user_administration.login'))
        user_id = userid_from_token(token)
        if not user_id:
            return redirect(url_for('user_administration.login'))


if __name__ == '__main__':
    app.run()
