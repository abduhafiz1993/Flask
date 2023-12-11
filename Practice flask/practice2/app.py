from flask import Flask, redirect, render_template, request
from cs50 import SQL

app = Flask(__name__)


db = SQL("sqlite:///students.db")

Sports=[]

SPORTS = db.execute("SELECT * FROM sports")
for row in SPORTS:
    Sports.append(row['name']) 

@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM students WHERE id = ?", id)
    return redirect("/registrants")

@app.route("/")
def index():
    return render_template("index.html", sports=Sports)

@app.route("/register", methods = ["POST"])
def register():

    sport=request.form.get("sport")

    name = request.form.get("name")

    if not name: 
        return render_template("faliure.html", message = "Missing name")
    elif not sport:
        return render_template("faliure.html", message = "Missing sport")
    elif not sport in Sports:
        return render_template("faliure.html", message = "Invalid sport")
    db.execute("INSERT INTO students (name, sport) VALUES (?, ?)", name, sport)

    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    REGISTRANTS=db.execute("SELECT * FROM students")
    return render_template("registrants.html", registrants = REGISTRANTS)

