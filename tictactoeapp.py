from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
#from flask_kvsession import KVSessionExtension
#from simplekv.memory.redisstore import RedisStore
#import redis

from tempfile import mkdtemp
import sys

app = Flask(__name__)
#app.run(host='0.0.0.0')
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANANET"] = False
app.config["SESSION_TYPE"] = "redis"
app.config["SECRET_KEY"] = "super secret key"
sess = Session(app)
#sess.init_app(app)


@app.route("/")
def load():
    return render_template("input.html")

@app.route("/start", methods=["GET", "POST"])
def start():
    print(f"start:  current value of session {session}")
    #app.logger.debug("Logging")
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
    print(f"index:  current value of session {session}")
    if "board" not in session:
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = session["player1"]
    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row,col):
        #turn = session["turn"]
        print(f"play current value of in session {session}")

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
        print(f"reset:  current value of session {session}")
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = session["player1"]
        print(f"reset  value of session {session}")
        sys.stdout.flush()
        return redirect(url_for("index"))

@app.route("/back")
def back():
        print(f"back:  current value of session {session}")
        session.pop("board")
        session.pop("turn")
        return redirect(url_for("load"))

if __name__ == "__main__":
    session.permanent = False
    app.run(debug = True)