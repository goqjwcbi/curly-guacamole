import sqlite3
import string
import random
import time

class Chat:

    #this class is not good i have no idea what im doing
    @staticmethod
    def addmsg(username, message):

        id = "".join(random.choice(string.ascii_letters) for i in range(8))

        query = "INSERT INTO messages VALUES(?, ?, ?, ?)"

        db_conn = sqlite3.connect("guacamole.db")
        db_cursor = db_conn.cursor()
        db_cursor.execute(query, (id, username, message, int(time.time())))
        db_conn.commit()
        db_conn.close()
