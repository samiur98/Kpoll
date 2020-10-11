# Import Statements
import requests
import json

def add_poll():
    # Makes HTTP request to cassandra server for adding a poll
    print("Bunnies")

def get_poll(username, title):
    # Makes HTTP request to cassandra server for getting a poll
    request_string = "http://127.0.0.1:5000/polls/{}/{}".format(username, title)
    response = requests.get(request_string)
    if response.status_code == 404:
        print("Poll with provided username and/or title not found")
    elif response.status_code == 500:
        print("Internal Server error, please try again later")
    else:
        print("Results for {} by {}".format(title, username))
        body = response.json()
        options_list = body["options"]
        votes_list = body["votes"]
        for i in range(0, len(options_list)):
            print("{}: {}".format(options_list[i], votes_list[i]))