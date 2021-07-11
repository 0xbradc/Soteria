import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# External helper.py file
from helpers import urlscan_api, google_api, risk, apology, login_required

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configures sql database to code
db = SQL("sqlite:///soteria.db")


# Method that uses sql statements to connect the website being scanned to the vulnerabilities that come up
def connect(vulnerability_data, website_rows):
    if vulnerability_data != None:
        for vuln in vulnerability_data:
            vuln_rows = db.execute("SELECT * FROM vulnerabilities WHERE type = ?;", vuln)
            if len(vuln_rows) == 0:
                db.execute("INSERT INTO vulnerabilities (type) VALUES(?);", vuln)
                vuln_rows = db.execute("SELECT * FROM vulnerabilities WHERE type = ?;", vuln)
            rows = db.execute("SELECT website_id FROM websites_vulnerabilities WHERE vulnerability_id = ?;", vuln_rows[0]["id"])
            if len(rows) == 0:
                db.execute("INSERT INTO websites_vulnerabilities (website_id, vulnerability_id) VALUES(?, ?);", website_rows[0]["id"], vuln_rows[0]["id"])


# Main homepage method once logged in
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # Stores the currently searched URL into the session
        session["url"] = request.form.get("url")
        return redirect("/results")

    else:
        return render_template("index.html")


# Returns the results of the website scan
@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    if request.method == "POST":
        session["url"] = request.form.get('url')
        return render_template("results.html", url=session["url"])

    else:
        # Checks if the inputted URL contains illegal characters or is too short
        if ("." not in session["url"] or "[" in session["url"] or "]" in session["url"]
        or "{" in session["url"] or "}" in session["url"] or "|" in session["url"]
        or "\\" in session["url"] or "*" in session["url"]
        or "~" in session["url"] or "`" in session["url"]
        or len(session["url"]) < 4):
            return apology("invalid website url", 403)

        else:
            urlscan_data = urlscan_api(session["url"])
            urlscan_message = urlscan_data["message"]
            urlscan_vulnerabilities = urlscan_data["data"]
            google_data = google_api(session["url"])
            google_message = google_data["message"]
            google_vulnerabilities = google_data["data"]

            risk_level = risk()

            # Add vulnerabilities to sql
            website_rows = []
            website_rows = db.execute("SELECT id FROM websites WHERE url = ?;", session["url"])
            if len(website_rows) == 0:
                db.execute("INSERT INTO websites (url) VALUES(?);", session["url"])
                website_rows = db.execute("SELECT id FROM websites WHERE url = ?;", session["url"])
            if len(db.execute("SELECT user_id FROM users_websites WHERE website_id = ?;", website_rows[0]["id"])) == 0:
                db.execute("INSERT INTO users_websites (user_id, website_id) VALUES(?, ?);", session["user_id"], website_rows[0]["id"])

            connect(google_vulnerabilities, website_rows)
            connect(urlscan_vulnerabilities, website_rows)

            # Checks if vulnerabilities are returned and returns correct information
            if urlscan_vulnerabilities != None and google_vulnerabilities != None:
                return render_template(
                    "results.html",
                    url=session["url"],
                    risk_level=risk_level,
                    urlscan_message=urlscan_message,
                    urlscan_vulnerabilities=urlscan_vulnerabilities,
                    google_message=google_message,
                    google_vulnerabilities=google_vulnerabilities
                )
            elif urlscan_vulnerabilities != None and google_vulnerabilities == None:
                return render_template(
                    "results.html",
                    url=session["url"],
                    risk_level=risk_level,
                    urlscan_message=urlscan_message,
                    urlscan_vulnerabilities=urlscan_vulnerabilities,
                    google_message=google_message
                )
            elif urlscan_vulnerabilities == None and google_vulnerabilities != None:
                return render_template(
                    "results.html",
                    url=session["url"],
                    risk_level=risk_level,
                    urlscan_message=urlscan_message,
                    google_message=google_message,
                    google_vulnerabilities=google_vulnerabilities
                )
            # Ran if there are not vulnerabilities
            else:
                return render_template(
                    "results.html",
                    url=session["url"],
                    risk_level=risk_level,
                    urlscan_message=urlscan_message,
                    google_message=google_message
                )


@app.route("/malware", methods=["GET"])
@login_required
def malware():
    return render_template("malware.html")


@app.route("/pha", methods=["GET"])
@login_required
def pha():
    return render_template("pha.html")


@app.route("/socialengineering", methods=["GET"])
@login_required
def socialengineering():
    return render_template("socialengineering.html")


@app.route("/vulnerabilitydictionary", methods=["GET"])
@login_required
def vulnerabilitydictionary():
    return render_template("dictionary_layout.html")


# Returns the user's history of searches
@app.route("/userdata", methods=["GET"])
@login_required
def userdata():

    counter = 0
    userdata_list = []
    websites = db.execute(
        "SELECT id, url FROM websites WHERE id IN (SELECT website_id FROM users_websites WHERE user_id = ?);",
        session["user_id"]
    )

    for website in websites:
        userdata_list.append({"url" : website["url"], "vulnerabilities" : []})

        vulns = db.execute("SELECT type FROM vulnerabilities WHERE id IN (SELECT vulnerability_id FROM websites_vulnerabilities WHERE website_id = ?);", website["id"])
        if len(vulns) != 0:
            for vuln in vulns:
                userdata_list[counter]["vulnerabilities"].append(vuln["type"])
        else:
            userdata_list[counter]["vulnerabilities"].append("No Known Vulnerabilities")
        counter += 1

    return render_template("userdata.html", userdata_list=userdata_list)


@app.route("/sources", methods=["GET"])
def sources():
    return render_template("sources.html")


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        # Forget any user_id
        session.clear()
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        user_hash = generate_password_hash(password)
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation matches
        elif password != confirmation:
            return apology("password must match confirmation", 400)

        # Ensures username is not already in database
        elif not db.execute("SELECT username FROM users WHERE username=(?)", username):
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, user_hash)
            return redirect("/login")
        else:
            return apology("this username is already used", 400)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
