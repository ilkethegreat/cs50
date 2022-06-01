import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    transactionsDB = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cashDB = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cashDB[0]["cash"]

    return render_template("index.html", database=transactionsDB, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        if not symbol:
            return apology("Invalid stock symbol.")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Invalid stock symbol.")
        elif not request.form.get("shares"):
            return apology("Invalid share amount.")
        if shares <= 0 and isinstance(shares, int) == False:
            return apology("Invalid transaction attempt.")

        transactionValue = shares * stock["price"]
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transactionValue:
            return apology("Not enough funds available for the transaction.")
        updatedBalance = user_cash - transactionValue

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updatedBalance, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"], date)
        flash("Share(s) purchased.")

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactionsDB = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactionsDB)


@app.route("/loadfunds", methods=["GET", "POST"])
@login_required
def loadfunds():
    """Let the user to load additional funds"""
    if request.method == "GET":
        return render_template("loadfunds.html")
    else:
        loadamount = int(request.form.get("loadamount"))
        if not loadamount:
            return apology("Invalid load amount.")

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        updatedBalance = user_cash + loadamount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updatedBalance, user_id)

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Invalid stock symbol.")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Invalid stock symbol.")
        return render_template("quoted.html", name=stock["name"], symbol=stock["symbol"], price=stock["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username must be entered.")
        if not password:
            return apology("Password must be entered.")
        if not confirmation:
            return apology("Please confirm the password.")
        if password != confirmation:
            return apology("Passwords must match.")

        hashPassword = generate_password_hash(password)

        try:
            newuser = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashPassword)
        except:
            return apology("Username is taken.")

        session["user_id"] = newuser
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        stocksymbolsuser = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in stocksymbolsuser])
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        if not symbol:
            return apology("Invalid stock symbol.")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Invalid stock symbol.")
        if shares <= 0:
            return apology("Invalid transaction attempt.")

        transactionValue = shares * stock["price"]
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        usershares = db.execute("SELECT shares FROM transactions WHERE id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        usersharesnet = usershares[0]["shares"]

        if shares > usersharesnet:
            return apology("Stock(s) not owned")

        updatedBalance = user_cash + transactionValue

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updatedBalance, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transaction (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], (-1) * shares, stock["price"], date)
        flash("Share(s) sold.")

        return redirect("/")
