# Import Statements
from flask import Blueprint, request, Response, jsonify
from util import create_response
from database import session

# Flask blueprint for polls
poll_api = Blueprint("poll_api", __name__)

# Route for getting a particular poll
@poll_api.route("/<username>/<title>", methods = ["GET"])
def get_poll(username, title):
    # Performs a GET request for a poll
    try:
        query = "SELECT * FROM poll_by_username_and_title WHERE username = '{}' AND title = '{}';".format(username, title)
        result = session.execute(query)
        return create_json_response(result)
    except IndexError:
        return create_response("Poll with username and title not found", 404)
    except Exception:
        return create_response("Internal Server Error", 500)

# Returns a properly formated dict containing the result of a GET query
def create_json_response(result):
    poll = result[0]
    body = {
        "username": poll.username,
        "title": poll.title,
        "id": poll.id,
        "options": poll.options,
        "votes": poll.votes
    }
    return jsonify(body)


# Route for adding a new poll
@poll_api.route("/", methods = ["POST"])
def add_poll():
    # Performs a POST request for adding a poll
    try:
        json = request.json
        username = json["username"]
        title = json["title"]
        options = json["options"]
        votes = json["votes"]

        if present(username, title):
            return create_response("Poll with provided username and title already exists", 401)
        
        query = "INSERT INTO poll_by_username_and_title (username, title, id, options, votes) "
        query = query + "VALUES ('{}', '{}', uuid(), {}, {});".format(username, 
                                                        title, options, votes)
        session.execute(query)
        return create_response("Poll Successfully added", 201)

    except (KeyError, AttributeError, TypeError):
        return create_response("Bad request with improper/incomplete fields", 403)
    except Exception:
        return create_response("Internal Server Error", 500)

# Returns True if poll with provided username and title exists, false otehrwise
def present(username, title):
    query = "SELECT * FROM poll_by_username_and_title WHERE username = '{}' AND title = '{}';".format(username, title)
    result = session.execute(query)
    for a in result:
        return True
    return False