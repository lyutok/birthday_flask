import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        name = request.form.get("name")
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))

        if not name or not month or not day:
            return redirect("/")

        if month not in range(1, 13) and day not in range(1, 32):
            return redirect("/")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # Display the entries in the database on index.html
        rows = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=rows)


@app.route("/delete", methods=["POST"])
def delete():

    # Delte row
    id = request.form.get("id")
    db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")
