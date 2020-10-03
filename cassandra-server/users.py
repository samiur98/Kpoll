# Import Statements
from flask import Blueprint, request, Response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Flask Blueprint for users
user_api = Blueprint("user_api", __name__)

# Route for getting a particular user from the database
@user_api.route("/verify", methods = ["POST"])
def verify_user():
    # Performs a POST request to verify a user
    try:
        json = request.json
        username = json["username"]
        password = json["password"]
        response =jsonify("User verfied")
        response.status_code = 200
        return response
    except (KeyError, AttributeError):
        response = jsonify("Bad request with improper/incomplete fields")
        response.status_code = 403
        return response


# Route for adding a particular user to the database
@user_api.route("/add", methods = ["POST"])
def add_user():
    # Performs a POST request to add a user
    try:
        json = request.json
        username = json["username"]
        password = json["password"]
        response = jsonify("User added successfully")
        response.status_code = 201
        return response
    except (AttributeError, KeyError):
        response = jsonify("Bad request with improper/incomplete fields")
        response.status_code = 403
        return response