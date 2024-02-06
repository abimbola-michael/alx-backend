#!/usr/bin/env python3
"""
Get locale from request
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from pytz import timezone
import pytz.exceptions


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


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Get user from request
    """
    try:
        return users.get(int(request.args.get("login_as")))
    except Exception:
        return None


@app.before_request
def before_request():
    """Before request"""
    user = get_user()
    if user:
        g.user = user


@babel.localeselector
def get_locale():
    """Gets locale from request"""
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    if g.user:
        locale = g.user.get("locale")
        if locale and locale in app.config["LANGUAGES"]:
            return locale
    locale = request.headers.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """Gets timezone from request"""
    time_zone = request.args.get("timezone")
    if time_zone:
        try:
            return timezone(time_zone).zone
        except Exception:
            pass
    try:
        if g.user:
            time_zone = g.user.get("timezone")
            if time_zone:
                return timezone(time_zone).zone
    except Exception:
        pass
    return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """GET method for the index route"""
    return render_template("7-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
