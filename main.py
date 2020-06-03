from flask import *
import sqlite3
import hashlib
from authentication import Authentication

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

app.secret_key = b"secret"

@app.route("/", methods = ["GET"])
def index():
    if 'user' in session:
        return "welcome %s" % session['user']
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

if __name__ == '__main__':
    app.run(debug = True,
            host="0.0.0.0")
