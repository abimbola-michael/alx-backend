#!/usr/bin/env python3
"""
Get locale from request
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """
    Config class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Gets locale from request"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """GET method for the index route"""
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
