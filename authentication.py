import sqlite3
import hashlib

class Authentication:
    @staticmethod
    def login(username, password):
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        print(password)

        conn = sqlite3.connect("guacamole.db")
        query = "SELECT uname FROM users WHERE uname = ? AND passwd = ?"
        c = conn.cursor()
        c.execute(query, (username, password))

        data = c.fetchone()
        conn.close()

        if data == None:
            return False
        else:
            return True

    @staticmethod
    def register(username, password):
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        if not Authentication.check_user_exists(username):
            query = "INSERT into users VALUES(?, ?)"

            db_conn = sqlite3.connect("guacamole.db")
            db_cursor = db_conn.cursor()
            db_cursor.execute(query, (username, password))
            db_conn.commit()
            db_conn.close()

            return True
            
        else:
            return False

    @staticmethod
    def check_user_exists(username):
        query = "SELECT uname FROM users WHERE uname = ? COLLATE NOCASE"
        conn = sqlite3.connect("guacamole.db")
        c = conn.cursor()
        c.execute(query, (username,))
        
        data = c.fetchone()
        conn.close()
        
        return (data != None)
