import sqlite3
import websocket
import hashlib
import time
import json
import threading
from flask import *

import client_websockets

from templates import *
from users import *
from chat import *
from action_validation import *

HOST = "0.0.0.0"
WEB_PORT = 8080
WS_PORT = 8090

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = b"secret"


@app.route("/", methods=["GET"])
def home():
    if "user" in session:
        return render_template("home.html", uname=session["user"])
    else:
        return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    uname = request.form["uname"]
    passwd = request.form["passwd"]

    if not (validate_username(uname) and validate_password(passwd)):
        return redirect(url_for("login") + "?invalid=bad_credentials")

    if authenticate_user(uname, passwd):
        session["user"] = uname
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login") + "?invalid=bad_credentials")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return redirect(url_for("home") + "?logout=true")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    uname = request.form["uname"]
    passwd = request.form["passwd"]

    if not (validate_username(uname) and validate_password(passwd)):
        return redirect(url_for("register") + "?invalid=bad_credentials")

    if register_user(uname, passwd):
        return redirect(url_for("home") + "?registered=true")
    else:
        return redirect(url_for("register") + "?invalid=bad_credentials")


@app.route("/chat", methods=["GET"])
def chat():
    if not validate_user(session["user"]):
        print(session["user"] + " is invalid")
        return redirect(url_for("register"))

    return render_template("chat.html")


@app.route("/api/v1/messages", methods=["GET", "POST"])
def api_messages():
    if request.method == "GET":
        messages = get_messages()

        json = "{\"messages\":["
        for i, message in enumerate(messages):
            json += "{\"id\":\"" + message[0] + "\","
            json += "\"author\":\"" + message[1] + "\","
            json += "\"content\":\"" + message[2] + "\","
            json += "\"time\":\"" + str(message[3]) + "\"}"

            if i != len(messages) - 1:
                json += ","
        json += "]}"
        return json

    elif request.method == "POST":
        if not validate_user(session["user"] or not validate_input(request.form["message"])):
            return error_page(400), 400

        uname = session["user"]
        message = request.form["message"]

        add_message(uname, message)
        return "OK"


def start_flask():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    client_websockets.listen()
