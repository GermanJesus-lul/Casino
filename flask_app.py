from flask import Flask, request, redirect

from blueprints.autodeployment import autodeployment
from blueprints.home import home
from blueprints.user_administration import user_administration

app = Flask(__name__)
app.register_blueprint(autodeployment)
app.register_blueprint(home)
app.register_blueprint(user_administration)


# force https
@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
