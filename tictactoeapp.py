from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import sys

app = Flask(__name__)
#app.run(host='0.0.0.0')
app.secret_key = "super secret key"

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
        #turn = session["turn"]
        print(f"current value of Turn {session}")
        session["board"][row][col] = session["turn"]
        print(f"current value of session {session}")
        if session["turn"] == "X":
            session["turn"] = "Y"
        elif session["turn"] == "Y":
            session["turn"] = "X"
        print(f"url   {url_for('index')}")
        sys.stdout.flush()
        return redirect(url_for("index"))

@app.route("/reset")
def reset():
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = "X"
        print(f"reset  value of session {session}")
        sys.stdout.flush()
        return redirect(url_for("index"))
