from flask import *
import sqlite3
import hashlib
from authentication import Authentication
from chat import Chat
import time

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

app.secret_key = b"secret"

@app.route("/", methods = ["GET"])
def index():
    if 'user' in session:
        return ("welcome %s" % session['user'])+'<br><a href="/chat">Chat</a>'
    else:
        return render_template("index.html")

@app.route("/p/<page>")
def visit_page(page):
    return render_template(page)
    
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]

        if Authentication.login(username, password):
            session['user'] = username
            return redirect(url_for("index"))
        else:
            return redirect("/p/login.html" + "?invalid=bad_credentials")

    else:
        return error("400", "Bad Request: This method is not supported for this request.")
        
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if Authentication.register(username, password):
            print("user logged in as %s" % username)
            return redirect("/p/login.html")
            
        else:
            return redirect("/p/register.html" + "?invalid=uname_taken")
    else:
        return error("400", "Bad Request: This method is not supported for this request.")

def error(err_code, err_desc):
    return render_template("error.html", error_code=err_code, error=err_desc)

@app.route("/chat", methods = ["GET", "POST"])
def chat():

    if not "user" in session:
        return redirect("/")
    
    if request.method == "POST":
        message = request.form["message"]
        username = session['user']
        send_msg(username, message)
        return redirect("/chat")
    else:
        return render_template("chat.html")

@app.route("/getmsg.json")
def getmsg():

    query_delete = "DELETE FROM messages WHERE time < " + str(int(time.time()) - 120)
    query_select = "SELECT * FROM messages"

    db_conn = sqlite3.connect("guacamole.db")
    db_cursor = db_conn.cursor()
    db_cursor.execute(query_delete)
    db_cursor.execute(query_select)

    messages = db_cursor.fetchall()

    db_conn.close()

    # yeah this is just bad...
    index = 0
    json = "{\"messages\":["
    for message in messages:
        json += "{"
        json += "\"id\": \"" + message[0] + "\","
        json += "\"author\":\"" + message[1] + "\","
        json += "\"content\":\"" + message[2] + "\","
        json += "\"time\":\"" + str(message[3]) + "\""
        json += "}"
        if index != len(messages) - 1:
            json += ","
        index += 1
    json += "]}"
    return json

def send_msg(username, message):
    #you can add<br> to the end of each message for new line
    #for now i added it to a list
    Chat.addmsg(username, message)
    
if __name__ == '__main__':
    app.run(debug = True,
            host="0.0.0.0")
