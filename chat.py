import sqlite3
import random
import string
import time
import asyncio

import client_websockets

import utils


def get_messages(room_id):
    query = "SELECT * FROM messages WHERE room = ?"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (room_id,))

    messages = db_cursor.fetchall()

    db_connect.close()

    return messages


def add_message(room_id, author_uname, message):
    id = utils.gen_id()

    query = "INSERT INTO messages VALUES (?, ?, ?, ?, ?)"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (id, room_id, author_uname,
                              message, int(time.time())))
    db_connect.commit()
    db_connect.close()

    broadcast_update()


def clear_messages(room_id):
    query = "DELETE FROM messages WHERE room = ?"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (room_id,))
    db_connect.commit()
    db_connect.close()

    broadcast_clear()


def handle_message(room_id, author_uname, message):

    if author_uname == "admin" and message.strip() == "_CLS":
        clear_messages(room_id)
    else:
        add_message(room_id, author_uname, message)


def get_rooms(owner):
    query = "SELECT * FROM rooms WHERE owner = ?"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (owner,))

    rooms = db_cursor.fetchall()

    db_connect.close()

    return rooms


def create_room(owner):
    id = utils.gen_id()

    query = "INSERT INTO rooms VALUES (?, ?)"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (id, owner))
    db_connect.commit()
    db_connect.close()

    return id


def validate_room(room_id):
    if room_id != None:
        query = "SELECT id FROM rooms WHERE id = ? COLLATE NOCASE"

        db_connect = sqlite3.connect("app.db")
        db_cursor = db_connect.cursor()
        db_cursor.execute(query, (room_id,))

        user = db_cursor.fetchone()

        db_connect.close()

        return user != None


def broadcast_clear():
    asyncio.run(client_websockets.broadcast("_CLS"))


def broadcast_update():
    asyncio.run(client_websockets.broadcast("_UPDATE"))
