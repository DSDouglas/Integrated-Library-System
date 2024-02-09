import requests
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/books")
def books():
    return render_template("books.html")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)