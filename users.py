import hashlib
import sqlite3
import random
import string


def authenticate_user(uname, passwd):
    passwd = hashlib.sha256(passwd.encode("utf-8")).hexdigest()

    query = "SELECT uname FROM users WHERE uname = ? AND passwd = ?"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (uname, passwd))

    user = db_cursor.fetchone()

    db_connect.close()

    return user != None


def register_user(uname, passwd):
    passwd = hashlib.sha256(passwd.encode("utf-8")).hexdigest()
    id = "".join(random.choice(string.ascii_letters) for i in range(8))

    if validate_user(uname):
        return False

    query = "INSERT INTO users (id, uname, passwd) VALUES (?, ?, ?)"

    db_connect = sqlite3.connect("app.db")
    db_cursor = db_connect.cursor()
    db_cursor.execute(query, (id, uname, passwd))

    db_connect.commit()
    db_connect.close()

    return True


def validate_user(uname):
    if uname != None:
        query = "SELECT uname FROM users WHERE uname = ?"

        db_connect = sqlite3.connect("app.db")
        db_cursor = db_connect.cursor()
        db_cursor.execute(query, (uname,))

        user = db_cursor.fetchone()

        db_connect.close()

        return user != None
