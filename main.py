import sqlite3
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
    if "user" in session and validate_user(session["user"]):
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
        return redirect("https://domain.tld/projects/apps/xe3/login?invalid=bad_credentials")

    if authenticate_user(uname, passwd):
        session["user"] = uname
        return redirect("https://domain.tld/projects/apps/xe3/")
    else:
        return redirect("https://domain.tld/projects/apps/xe3/login?invalid=bad_credentials")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    return redirect("https://domain.tld/projects/apps/xe3/?logout=true")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    uname = request.form["uname"]
    passwd = request.form["passwd"]

    if not (validate_username(uname) and validate_password(passwd)):
        return redirect("https://domain.tld/projects/apps/xe3/register?invalid=bad_credentials")

    if register_user(uname, passwd):
        return redirect("https://domain.tld/projects/apps/xe3/?registered=true")
    else:
        return redirect("https://domain.tld/projects/apps/xe3/register?invalid=bad_credentials")


@app.route("/rooms", methods=["GET"])
def rooms():
    if not session or not validate_user(session["user"]):
        return redirect("https://domain.tld/projects/apps/xe3/register")

    return render_template("rooms.html")


@app.route("/rooms/<room_id>", methods=["GET"])
def room(room_id):
    if not session or not validate_user(session["user"]):
        return redirect("https://domain.tld/projects/apps/xe3/register")

    if not validate_room(room_id):
        return error_page(404, "Room not found"), 404

    return render_template("chat.html", room_id=room_id)


@app.route("/api/v1/rooms", methods=["GET", "POST"])
def api_rooms():

    if not session or not validate_user(session["user"]):
        return error_page(400, error_desc="Bad Request"), 400

    if request.method == "POST":
        new_room_id = create_room(session["user"])
        return new_room_id, 201
    elif request.method == "GET":
        rooms = get_rooms(session["user"])

        json = "{\"rooms\":["
        for i, message in enumerate(rooms):
            json += "{\"id\":\"" + message[0] + "\"}"
            if i != len(rooms) - 1:
                json += ","
        json += "]}"
        return json


@app.route("/api/v1/rooms/<room_id>/messages", methods=["GET", "POST"])
def api_room_messages(room_id):

    if not validate_room(room_id):
        return error_page(404), 404

    if request.method == "GET":
        messages = get_messages(room_id)

        # ...what....
        json = "{\"messages\":["
        for i, message in enumerate(messages):
            json += "{\"id\":\"" + message[0] + "\","
            json += "\"author\":\"" + message[2] + "\","
            json += "\"content\":\"" + sanitize_json(message[3]) + "\","
            json += "\"time\":" + str(message[4]) + "}"

            if i != len(messages) - 1:
                json += ","
        json += "]}"
        return json
    elif request.method == "POST":
        if not session or not validate_user(session["user"] or not validate_input(request.form["message"])):
            return error_page(400, error_desc="Bad Request"), 400

        uname = session["user"]
        message = request.form["message"]

        handle_message(room_id, uname, message)
        return "OK"


def start_flask():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    client_websockets.listen()
