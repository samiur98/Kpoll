# Import Statements
from flask import Blueprint, request, Response, jsonify

# Flask blueprint for polls
poll_api = Blueprint("poll_api", __name__)

# Route for getting a particular poll
@poll_api.route("/<username>/<title>", methods = ["GET"])
def get_poll(username, title):
    # Performs a GET request for a poll
    response = jsonify("here is your poll")
    response.status_code = 200
    return response


# Route for adding a new poll
@poll_api.route("/", methods = ["POST"])
def add_poll(username, title):
    # Performs a POST request for adding a poll
    try:
        json = request.json
        username = json["username"]
        title = json["title"]
        options = json["options"]
        votes = json["votes"]
        response = jsonify("New poll successfully added!")
        response.status_code = 201
        return response
    except (KeyError, AttributeError):
        response = jsonify("Bad request with improper/incomplete fields")
        response.status_code = 403
        return response

# Route for closing a particular poll
@poll_api.route("/<username>/<title>", methods = ["PUT"])
def close_poll(username, title):
    # Performs a PUT request for closing a poll
    response = jsonify("Poll successfully closed")
    response.status_code = 200
    return response
