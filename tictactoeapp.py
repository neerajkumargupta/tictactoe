from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from tempfile import mkdtemp
import sys

app = Flask(__name__)
#app.run(host='0.0.0.0')
app.secret_key = "super secret key"
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANANET"] = False
#app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "super secret key"
sess = Session(app)
#sess.init_app(app)
#session.permanent = False

@app.route("/", methods=['GET','POST'])
def load():
    if request.method == 'POST':
        player1=request.form['Player1']
        player2=request.form['Player2']
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = player1   


    return redirect(url_for("index",player1,player2))

@app.route("/game")
def index(player1, player2):
    
    if "board" not in session:
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = player1
    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row,col):
        #turn = session["turn"]
        print(f"current value of Turn {session}")
        session["board"][row][col] = session["turn"]
        print(f"current value of session {session}")
        if session["turn"] == player1:
            session["turn"] = player2
        elif session["turn"] == player2:
            session["turn"] = player1
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

@app.route("/back")
def back():
        session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        session["turn"] = None
        return redirect(url_for("load"))

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    session.permanent = False
    sess.init_app(app)
    app.debug = True
    app.run()