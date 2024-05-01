from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/play", methods=["POST"])
def play():
    global playername
    if request.method == "POST":
        playername = request.form["playername"]
    return render_template("play.html", playername = playername)