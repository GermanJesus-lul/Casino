from flask import Flask, render_template, request

app = Flask(__name__)


def valid_login(username, password):
    return True


def register_user(username, password):
    pass


@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if valid_login(username, password):
            return "success"
        return "failed"
    elif request.method == "GET":
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)