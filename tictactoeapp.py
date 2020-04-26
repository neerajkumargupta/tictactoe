from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
app.run(host='0.0.0.0')

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANANET"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.route("/")
def index():
    
    if "board" not in session:
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = "X"
    
    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row,col):
        turn = session["turn"]
        session["board"][row][col] = turn
        
        if turn == "X":
            session["turn"] = "Y"
        elif turn == "Y":
            session["turn"] = "X"

        return redirect(url_for("index"))

@app.route("/reset")
def reset():
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = "X"
        return redirect(url_for("index"))
