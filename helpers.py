import os
import requests
import urllib.parse
import json
import time
import requests

from flask import redirect, render_template, request, session
from functools import wraps

# Seconds for waiting for API to load
WAIT_TIME = 25

# Global variable used for ranking threats
count = 0


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", " "), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=(escape(message).capitalize())), code


# Method for connecting to the URLScan.io API and returning its results
# Documentation can be found at https://urlscan.io/about-api/
def urlscan_api(input_url):
    global count

    try:
        headers = {'API-Key':'e138677d-28fd-4a9e-8ffd-0fba8b942aa1','Content-Type':'application/json'}
        data = {"url": input_url, "visibility": "public"}
        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
        response.raise_for_status()

    except requests.RequestException:
        print("FIRST EXCEPTION RAISED_urlscan")
        return {
            "message": "<p style=\"color: red;\">Failure with API. Please contact customer support.</p>",
            "data": None
        }

    try:
        data = response.json()

        # Wait for server to populate results
        time.sleep(WAIT_TIME)

        # Get data from API on security risks
        verdicts = requests.get(data["api"]).json()["verdicts"]
        if verdicts["overall"]["score"] == 0:
            return {
                "message": "<p style=\"color:green;\">This website is low risk.</p>",
                "data": None
            }
        else:
            count += 1
            print(verdicts["overall"])
            return {
                "message": "<p style=\"color: red;\">This website is at risk for security vulnerabilities.</p>",
                "data": verdicts["overall"]["categories"]
            }

    except (KeyError, TypeError, ValueError):
        print("SECOND EXCEPTION RAISED_urlscan")
        return {
            "message": "<p style=\"color: red;\">Failure with API. Please contact customer support.</p>",
            "data": None
        }


# Method for connecting to the Google Safe Browsing API and returning its results
# Documentation can be found at https://developers.google.com/safe-browsing
def google_api(input_url):
    global count
    headers = {'Content-Type':'application/json'}
    post_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyBU3AL1VIV-UCZ0kuDVVbWzWFAdhlrNKuM"
    data = {
        "client": {
            "clientId": "college.harvard.edu",
            "clientVersion": "1.5.2"
        },
        "threatInfo": {
            "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION", "UNWANTED_SOFTWARE", "THREAT_TYPE_UNSPECIFIED"],
            "platformTypes":    ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": input_url}
            ]
        }
    }
    response = requests.post(post_url, headers=headers, data=json.dumps(data))

    try:
        data = response.json()

        if len(data) < 1:
            return {
                "message": "<p style=\"color:green;\">This website is low risk.</p>",
                "data": None
            }
        else:
            count += 1
            vulns = []
            for match in data["matches"]:
                vulns.append(match["threatType"])
            return {
                "message": "<p style=\"color: red;\">This website is at risk for security vulnerabilities.</p>",
                "data": vulns
            }

    except (KeyError, TypeError, ValueError):
        print("FIRST EXCEPTION RAISED_google")
        return {
            "message": "<p style=\"color: red;\">Failure with API. Please contact customer support.</p>",
            "data": None
        }


# Method for returning the risk level of the website
def risk():
    global count
    if count == 0:
        return ("<p style=\"color:green;\">Low Risk</p>")
    elif count == 1:
        return ("<p style=\"color:yellow;\">Medium Risk</p>")
    else:
        return ("<p style=\"color:red;\">High Risk</p>")
