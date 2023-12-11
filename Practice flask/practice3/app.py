from flask import Flask, request, redirect, render_template, session 
from cs50 import SQL
from flask_session import Session


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")

@app.route("/register", methods=["POST", "GET"] )
def reg():
    if request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")
        if not username or not password:
            return render_template("faliure.html", message = "Write password and username")
        user = db.execute("select username from users where username = ?", username)
        if username == user:
            return render_template("faliure.html", message = "you have account already.")
        db.execute("INSERT INTO USERS (username, password) VALUES (?, ?)", username, password)
        session['name'] = username
        return redirect("/")

    return render_template("register.html")

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    books = db.execute("SELECT * FROM books")
    return render_template("index.html", books = books)

@app.route("/favorite", methods=["POST", "GET"])
def favriote():
    if not session["favriote"] in session:
        session["favriote"] = []
    
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            if not id  in session["favriote"]
            session["favriote"].append(id)

    books = db.execute("SELECT * FROM users where id in ?", session["favriote"])
    return render_template("favroite.html", books = books)    

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")
        if not username or not password:
            return render_template("/failure.html", message="Please fill in both username and password.")

        users = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        # Check if a user with the specified username exists
        user = users[0]

        if user is None or user['password'] != password:
            return render_template("/failure.html", message="Invalid username or password. Please check your credentials.")

        # Authentication successful, store the username in the session
        session["name"] = username
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session['name'] = None
    return redirect("/")

@app.route("/rem", methods=["POST"])
def removess():
    id = int(request.form.get("id"))
    if id:
        if "favriote" in session and id in session["favriote"]:
            session["favriote"].remove(id)
        books = db.execute("SELECT * FROM users where id in ?", session["favriote"])
        return redirect("/favriote", books = books)
    return redirect("/favriote")
