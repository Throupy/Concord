"""Main application."""

from flask import render_template
from concord import app


@app.route("/")
def home():
    """Home route."""
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
