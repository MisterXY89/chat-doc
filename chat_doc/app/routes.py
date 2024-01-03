"""
Contains all the routes for the app
"""

from flask import (
    Blueprint,
    Response,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

# Create a Blueprint
routes_blueprint = Blueprint("routes_blueprint", __name__)


@routes_blueprint.route("/")
def home():
    return render_template("index.html")
