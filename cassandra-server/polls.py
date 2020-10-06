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
        query = "SELECT * FROM polls_by_username_and_title WHERE username = '{}' AND title = '{}';".format(username, title)
        print(query)
        result = session.execute(query)
        return create_json_response(result)
    except Exception:
        return create_response("Internal Server Error", 500)

# Returns a properly formated dict containing the result of a GET query
def create_json_response(result):
    if result == 0:
        return create_response("Poll with username and title not found", 404)
    poll = result[0]
    print(poll)
    return {
        "username": poll.username,
        "title": poll.title,
        "id": poll.id,
        "open": poll.open,
        "options": poll.options,
        "votes": poll.votes
    }


# Route for adding a new poll
@poll_api.route("/", methods = ["POST"])
def add_poll():
    # Performs a POST request for adding a poll
    try:
        json = request.json
        username = json["username"]
        title = json["title"]
        options = json["options"]
        if present(username, title):
            return create_response("Poll with provided username and title already exists", 403)
        
        query = "INSERT INTO polls_by_username_and_title (username, title, id, open, options, votes) "
        query = query + "VALUES ('{}', '{}', uuid(), true, {}, {});".format(username, 
                                                        title, options, getZeroList(len(options)))
        session.execute(query)
        return create_response("Poll Successfully added", 201)

    except (KeyError, AttributeError):
        return create_response("Bad request with improper/incomplete fields", 403)
    except Exception:
        return create_response("Internal Server Error", 500)

# Returns a list of n 0's
def getZeroList(n):
    result = []
    i = n
    while(i > 0):
        result.append(0)
        i = i - 1
    return result


# Route for closing a particular poll
@poll_api.route("/", methods = ["PUT"])
def close_poll():
    # Performs a PUT request for closing a poll
    try:
        json = request.json
        username = json["username"]
        title = json["title"]
        votes = json["votes"]
        if not present(username, title):
            return create_response("Poll with provided username and title does not exist", 404)
        
        query = "UPDATE polls_by_username_and_title SET open={}, votes={} WHERE username='{}' AND title='{}';".format("false", 
                                                                    votes, username, title)
        session.execute(query)
        return create_response("Poll Successfully closed", 200)

    except (KeyError, AttributeError):
        return create_response("Bad request with improper/incomplete fields", 403)
    except Exception:
        print(Exception)
        return create_response("Internal Server Error", 500)

# Returns True if poll with provided username and password exists, false otehrwise
def present(username, title):
    query = "SELECT * FROM polls_by_username_and_title WHERE username = '{}' AND title = '{}';".format(username, title)
    result = session.execute(query)
    for a in result:
        return True
    return False