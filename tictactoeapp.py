from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from tempfile import mkdtemp
import sys

app = Flask(__name__)
#app.run(host='0.0.0.0')
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANANET"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "super secret key"
Session(app)
#sess.init_app(app)
#session.permanent = False
#player1 = None
#player2 = None

@app.route("/")
def load():
    return render_template("input.html")

@app.route("/start", methods=["GET", "POST"])
def start():
    player1 = request.form.get("Player1", "X")
    player2 = request.form.get("Player2", "Y")
    
    print(f"Player 1   {player1}")
    print(f"Player 2   {player2}")
    print(f"Session   {session}")
    
    session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
    session["turn"] = player1
    session["player1"] = player1
    session["player2"] = player2
    
    print(f"Session 2   {session}")
    sys.stdout.flush()
    return redirect(url_for("index"))

@app.route("/game")
def index():
    
    if "board" not in session:
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = session["player1"]
    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row,col):
        #turn = session["turn"]
        print(f"current value of Turn in session {session}")

        session["board"][row][col] = session["turn"]
        print(f"current value of session {session}")
        print("Player 1  " +  session["player1"])
        print("Player 2  " +  session["player2"])
        if session["turn"] == session["player1"]:
            session["turn"] = session["player2"]
        elif session["turn"] == session["player2"]:
            session["turn"] = session["player1"]
        print(f"url   {url_for('index')}")
        sys.stdout.flush()
        return redirect(url_for("index"))

@app.route("/reset")
def reset():
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = session["player1"]
        print(f"reset  value of session {session}")
        sys.stdout.flush()
        return redirect(url_for("index"))

@app.route("/back")
def back():
        session.pop("board")
        session.pop("turn")
        return redirect(url_for("load"))

if __name__ == "__main__":
    #app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    #session.permanent = False
    app.debug = True
    app.run()