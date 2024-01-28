from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "<h1>Hello World!</h1>"
    elif request.method == "GET":
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)