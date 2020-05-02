#!/usr/bin/env python

from flask import Flask
from flask import redirect
from flask import render_template as rt
from flask import request

import omdb
import argparse
import os
import random

# initialize app
app = Flask(__name__)

OPTIONS = [
    "house of cards",
    "when they see us",
    "queen of the south",
    "money heist",
    "lost",
    "you",
    "breaking bad"
]

@app.route("/", methods=["GET", "POST"])
def index():
    """
    main route
    """
    if request.method == "GET":
        suffix = str(random.choice(OPTIONS)).lower().replace(" ", "-")
    else:
        suffix = str(request.form["q"]).lower().replace(" ", "-")

    return redirect("/%s" % (suffix))

@app.route("/<string:title>")
def search(title):
    """
    search route
    """
    data = omdb.find_by_title(title.replace("-", " "))

    if not data:
        data = omdb.find_by_title(random.choice(OPTIONS))
        found = False
    else:
        found = True
    
    labels = []
    values = []

    i = 1
    for episode in data["episodes"]:
        labels.append(i)
        values.append({
            "x": i,
            "y": episode["imdb"]["rating"]
        })
        i += 1

    return rt("search.html", data=data, labels=labels, values=values, found=found)

@app.route("/not-found", methods=["GET"])
def not_found():
    """
    series not found route
    """
    return rt("not-found.html")

def config_parser():
    """
    config app parser
    """
    parser = argparse.ArgumentParser(__name__)

    parser.add_argument("-d", "--debug", help="run in debug mode (default: %(default)s)", action="store_true", required=False)
    parser.add_argument("-p", "--port", help="run on port (default: %(default)s)", default=5000, required=False)

    return parser

if __name__ == "__main__":
    """
    main function
    """
    args = config_parser().parse_args()

    if args.debug:
        os.environ["FLASK_ENV"] = "development"

    try:
        app.run(**{
            "host": "0.0.0.0",
            "debug": args.debug,
            "port": args.port
        })

    except Exception as e:
        print(str(e))