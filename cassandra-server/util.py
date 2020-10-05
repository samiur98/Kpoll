from flask import jsonify

# Utility function that returns a properly formatted response to an HTTP request
def create_response(message, status_code):
    response = jsonify(message)
    response.status_code = status_code
    return response