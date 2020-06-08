import sqlite3
import random
import string
import time
import asyncio

import client_websockets


def get_messages():
    query = "SELECT * FROM messages"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query)

    messages = db_cursor.fetchall()

    db_connect.close()

    return messages


def add_message(uname, message):
    id = "".join(random.choice(string.ascii_letters) for i in range(8))

    query = "INSERT INTO messages VALUES(?, ?, ?, ?)"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (id, uname, message, int(time.time())))
    db_connect.commit()
    db_connect.close()

    broadcast_update()


def broadcast_update():
    asyncio.run(client_websockets.broadcast("_update"))
