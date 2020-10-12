# Import Statements
import requests

def register_user(username, password):
    # Makes HTTP request to cassandra server to add a new user.
    body = {
        'username': username,
        'password': password
    }
    response = requests.post('http://127.0.0.1:5000/users/add', 
                        json = body)
    if response.status_code == 201:
        print("You have been Successfully Registered!")
    elif response.status_code == 403:
        print("You have not entered username and/or password correctly")
    elif response.status_code == 401:
        print("User with provided username already exists, please try another username")
    else:
        print("Internal server error, we could not register you, please try again later")

def verify_user(username, password):
    # Makes HTTP request to cassandra server to verify user's credentials.
    body = {
        'username': username,
        'password': password
    }
    response = requests.post('http://127.0.0.1:5000/users/verify', json = body)
    return response.status_code

        