import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request

# Configure application
app = Flask(__name__)

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
        # Add a new birthday
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if not name or not month or not day:
            flash("All fields are required!")
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
            if month < 1 or month > 12 or day < 1 or day > 31:
                flash("Invalid date!")
                return redirect("/")
        except ValueError:
            flash("Invalid input!")
            return redirect("/")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect("/")

    else:
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)

@app.route("/edit", methods=["POST"])
def edit():
    # Update the birthday in the database
    id = request.form.get("id")
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")

    # Validate inputs
    if not name or not month or not day:
        flash("All fields are required!")
        return redirect("/")

    db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?",
               name, int(month), int(day), id)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")

    db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")
