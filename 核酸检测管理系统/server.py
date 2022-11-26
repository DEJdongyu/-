from flask import Flask, render_template

app = Flask(__name__)


@app.route("/",methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/templates/user1.html",methods=["GET", "POST"])
def user1():
    return render_template("user1.html")


if __name__ == "__main__":
    app.run(debug=True)
