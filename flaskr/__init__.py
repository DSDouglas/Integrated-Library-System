import requests
import os
import mariadb
from flask import Flask, redirect, render_template, request, session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def home_page():
        return render_template("index.html")

    return app

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/books")
    def books():
        return render_template("books.html")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
