from flask import Flask, request
import sqlite3
import hashlib

app = Flask(__name__,
            static_url_path='',
            static_folder='static')


@app.route("/")
def index():
    if 'user' in session:
        return "welcome %s" % session['user']
    else:
        return render_template("index.html")
    
@app.route("/login", methods = ["GET", "POST"])
def login():
    if method == "POST":
        username = request.args.get("username")
        password = hashlib.sha256(request.args.get("password")).hexdigest()

        c = sqlite.conn("guacamole.db").cursor()
        query = "SELECT username FROM users WHERE name = ? AND password = ?"
        c.execute(query, username, password)
        data = c.fetchone()
        if data == None:
            printf("failed to log in as %s" % username)
        else:
            session['user'] = username
        redirect(url_for(""))
    else:
        return "unsupportted method"
        
@app.route("/register", methods = ["GET", "POST"])
def register():
    if method == "POST":
        username = request.args.get("username")
        password = request.args.get("password")
        if not check_user_exists(username):
            query = "INSERT INTO users VALUES (?, ?)"
            c = sqlite.conn("guacamole.db").cursor()
            c.execute(query, username, password)
            redirect(url_for(""))
        else:
            return error("user already exists")
    else:
        return "unsupported method"


def error(e):
    return render_template("error.html", error = e)
            
def check_user_exists(username):
    c = sqlite.conn().cursor()
    query = "SELECT username FROM users WHERE name = ?"
    c.execute(query, username)
    data = c.fetchone()
    if data == None:
        return False
    else:
        return True
if __name__ == '__main__':
    app.run(debug = True)