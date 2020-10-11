# Import Statements
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from database import session
from util import create_response

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
        query = "SELECT * FROM user_by_username WHERE username = '{}';".format(username)
        result = session.execute(query)
        for entry in result:
            if check_password_hash(entry.password, password):
                return create_response("User Verfied", 200)
            else:
                return create_response("User not verfied", 404)
        return create_response("User not found", 404)

    except (KeyError, AttributeError):
        return create_response("Bad request with improper/incomplete fields", 403)
    except Exception:
        return create_response("Internal Server Error", 500)

# Route for adding a particular user to the database
@user_api.route("/add", methods = ["POST"])
def add_user():
    # Performs a POST request to add a user
    try:
        json = request.json
        username = json["username"]
        password = generate_password_hash(json["password"])
        if present(username):
            return create_response("User with provided username already exists", 401)
        query = "INSERT INTO user_by_username (id, username, password) VALUES (uuid(), '{}', '{}');".format(username, password)
        session.execute(query)
        return create_response("User added successfully", 201)
        
    except (AttributeError, KeyError):
        return create_response("Bad request with improper/incomplete fields", 403)
    except Exception:
        return create_response("Internal server serror", 500)

# Returns True if poll with provided username and title exists, false otehrwise
def present(username):
    query = "SELECT * FROM user_by_username WHERE username = '{}';".format(username)
    result = session.execute(query)
    for a in result:
        return True
    return False