class chat:
    #this class is not good i have no idea what im doing
    def addmsg(self,message):
        query = "message"

        db_conn = sqlite3.connect("chat.db")
        db_cursor = db_conn.cursor()
        db_cursor.execute(query, (username, password))
        db_conn.commit()
        db_conn.close()
