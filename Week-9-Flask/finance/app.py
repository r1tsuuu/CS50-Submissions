import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
from datetime import datetime, timezone

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create new table for orders and index for efficient search
db.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER,
        user_id NUMERIC NOT NULL,
        symbol TEXT NOT NULL,
        shares NUMERIC NOT NULL,
        price NUMERIC NOT NULL,
        timestamp TEXT,
        PRIMARY KEY(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")
db.execute("CREATE INDEX IF NOT EXISTS orders_by_user_id_index ON orders (user_id)")

# Ensure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    owns = own_shares()
    total = 0
    for symbol, shares in owns.items():
        result = lookup(symbol)
        name, price = result["name"], result["price"]
        stock_value = shares * price
        total += stock_value
        owns[symbol] = (name, shares, usd(price), usd(stock_value))
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
    total += cash
    return render_template("index.html", owns=owns, cash=usd(cash), total=usd(total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    symbol = request.form.get("symbol").strip()  # Strip spaces around the symbol

    if not symbol:
        return apology("Please provide a valid ticker symbol", 400)

    result = lookup(symbol)

    if not result:
        return apology(f"Invalid symbol: {symbol}", 400)

    try:
        shares = int(request.form.get("shares"))  # Convert shares to integer
    except ValueError:
        return apology("Shares must be a number", 400)

    # Check if shares is less than or equal to zero
    if shares <= 0:
        return apology("Shares must be a positive number", 400)

    name = result["name"]
    price = result["price"]
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
    remain = cash - price * shares
    if remain < 0:
        return apology("Insufficient Cash. Failed Purchase.")

    db.execute("UPDATE users SET cash = ? WHERE id = ?", remain, user_id)

    db.execute("INSERT INTO orders (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)", \
                                     user_id, symbol, shares, price, time_now())

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, shares, price, timestamp FROM orders WHERE user_id = ?", session["user_id"])

    transactions = []
    for row in rows:
        transactions.append({
            "symbol": row["symbol"],
            "shares": row["shares"],
            "price": usd(row["price"]),
            "timestamp": row["timestamp"]
        })

    return render_template("history.html", rows=transactions)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return apology("Must provide username and password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    symbol = request.form.get("symbol").strip()  # Strip any extra spaces from the symbol

    # Check if the symbol is empty
    if not symbol:
        return apology("Please provide a valid ticker symbol", 400)

    result = lookup(symbol)

    # Check if the symbol is invalid (lookup returns None)
    if not result:
        return apology(f"Invalid symbol: {symbol}", 400)

    return render_template("quoted.html", name=result["name"], price=usd(result["price"]), symbol=result["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username or len(db.execute('SELECT username FROM users WHERE username = ?', username)) > 0:
        return apology("Invalid Username: Blank, or already exists")
    if not password or password != confirmation:
        return apology("Invalid Password: Blank, or does not match")

    db.execute('INSERT INTO users (username, hash) VALUES(?, ?)', username, generate_password_hash(password))
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    session["user_id"] = rows[0]["id"]
    return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock; Similar to /buy, with negative # shares"""
    owns = own_shares()  # Get the user's owned shares

    if request.method == "GET":
        return render_template("sell.html", owns=owns.keys())

    symbol = request.form.get("symbol")
    shares_input = request.form.get("shares")

    # Check if shares input is numeric and positive
    if not shares_input.isdigit() or int(shares_input) <= 0:
        return apology("Invalid number of shares. Must be a positive integer.", 400)  # Invalid input, 400 error

    shares = int(shares_input)

    if owns.get(symbol, 0) < shares:
        return render_template("sell.html", invalid=True, symbol=symbol, owns=owns.keys())

    result = lookup(symbol)
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
    price = result["price"]
    remain = cash + price * shares

    db.execute("UPDATE users SET cash = ? WHERE id = ?", remain, user_id)

    db.execute("INSERT INTO orders (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
               user_id, symbol, -shares, price, time_now())

    return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

def own_shares():
    """Helper function: Which stocks the user owns"""
    user_id = session["user_id"]
    owns = {}
    query = db.execute("SELECT symbol, shares FROM orders WHERE user_id = ?", user_id)
    for q in query:
        symbol, shares = q["symbol"], q["shares"]
        owns[symbol] = owns.get(symbol, 0) + shares
    return {k: v for k, v in owns.items() if v != 0}

def time_now():
    """Helper: Get current UTC date and time"""
    now_utc = datetime.now(timezone.utc)
    return f"{now_utc.date()} @time {now_utc.time().strftime('%H:%M:%S')}"
