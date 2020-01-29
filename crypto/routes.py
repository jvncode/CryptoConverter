from crypto import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/purchase")
def current():
    return render_template("purchase.html")


@app.route("/status")
def inverter():
    return render_template("status.html")
