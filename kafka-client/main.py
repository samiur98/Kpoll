# Import Statements
from users import register_user, verify_user
from polls import get_poll, add_poll
from producer import create_producer
from consumer import create_consumer
from json import dumps
from kafka.admin import KafkaAdminClient, NewTopic

def main():
    print_welcome_message()
    cmd = ""
    off = False
    while not off:
        cmd = input()
        if cmd == "Q":
            print("Thank-you")
            off = True
        elif cmd == "N":
            register_new_user_loop()
        elif cmd == "S":
            see_prev_poll_loop()
        elif cmd == "V":
            vote_on_poll()
        elif cmd == "A":
            start_poll()
        else:
            print("Invalid Option")
            print_options()

def register_new_user_loop():
    # Provides I/O for adding a new user and calls register_user
    print("Please enter username")
    username = input()
    print("Please enter password")
    password = input()
    register_user(username, password)

def see_prev_poll_loop():
    # Provides I/O for seeing the results of a previous poll and calls get_poll
    print("Please enter the title of the poll")
    title = input()
    print("Please enter the username of the creator or author of the poll")
    username = input()
    get_poll(username, title)

def vote_on_poll():
    # Provides I/O for voting on a poll, Creates a kafka producer and sends a message to the producer representing a vote
    print("Please Enter the title of the poll")
    title = input()
    print("Please enter the username of the creator or author of the poll")
    username = input()
    print("Please enter the option that you would like to vote for")
    option = input()
    producer = create_producer()
    producer.send("{}-{}".format(username, title), str.encode(option))
    print("Thank-you for voting!")
    producer.close()

def start_poll():
    # Provides I/O for starting a poll, Verifies user through the cassandra server.
    # Records Votes through the Kafka Consumer, soon as vote is finished persists the data long term through the cassandra server.
    print("Please enter your username. You must be a registered user to create a poll")
    username = input()
    print("Please Enter your password")
    password = input()
    status_code = verify_user(username, password)
    start_poll_helper(status_code, username)

def start_poll_helper(status_code, username):
    # Proceeds forward with starting poll based on the result of verification via cassandra server
    if status_code == 200:
        user_verified_loop(username)
    elif status_code == 403:
        print("Username and/or Password was not entered correctly, please try again")
    elif status_code == 404:
        print("User could not be verified. Either the username and/or password is incorrect")
    else:
        print("Internal server error, please try again later")

def user_verified_loop(username):
    # Proceeds forward with starting a poll after a user has been verfied
    try:
        print("Please enter the title of your poll")
        title = input()
        print("Please enter the options of your poll seperated by spaces")
        options = input().split()
        votes = get_initial_votes(len(options))
        print("Please enter how long you want the poll to be active in seconds")
        time = int(input()) * 1000
        add_topic(username, title)
        consumer = create_consumer("{}-{}".format(username, title), time)
        for message in consumer:
            for i in range(0, len(options)):
                if message.value == str.encode(options[i]):
                    votes[i] = votes[i] + 1
        consumer.close()
        delete_topic(username, title)
        status_code = add_poll(username, title, options, votes)
        close_poll_loop(status_code, options, votes)

    except ValueError:
        print("You must enter a valid number for how long you wnat the poll to last in seconds")

def close_poll_loop(status_code, options, votes):
    # Provides a response to user after performing HTTP request for adding poll to cassandra server
    if status_code == 201:
        display_result(options, votes)
    elif status_code == 401:
        print("Poll with provided username and title already exists")
    elif status_code == 403:
        print("Fields not provided correctly")
    else:
        print("Internal server error, please try again later")

def display_result(options, votes):
    # Displays results of a poll
    print("Poll closed, here are the results")
    for i in range(0, len(options)):
        print("{}: {}".format(options[i], votes[i]))

def get_initial_votes(n):
    # Returns a list conatining n amounts of 0's
    result = []
    for i in range(0, n):
        result.append(0)
    return result

def add_topic(username, title):
    # Creates a new kafka topic, based on username and title
    admin_client = KafkaAdminClient(bootstrap_servers = 'localhost:9092')
    topic_lst = []
    topic_name = "{}-{}".format(username, title)
    topic_lst.append(NewTopic(name = topic_name, num_partitions = 1, replication_factor = 1))
    admin_client.create_topics(topic_lst)

def delete_topic(username, title):
    # Deletes a kafak topic, based on username and title
    admin_client = KafkaAdminClient(bootstrap_servers = 'localhost:9092')
    topic_lst = []
    topic_name = "{}-{}".format(username, title)
    topic_lst.append(topic_name)
    admin_client.delete_topics(topic_lst)

def print_welcome_message():
    # Prints Welcome message
    print("Welcome to Kpoll")
    print_options()

def print_options():
    # Prints the avilable options
    print("Please select one of the following options")
    print("Press A to start a poll")
    print("Press S to see results of a poll")
    print("Press N to register as a new user")
    print("Press V to vote on a poll")
    print("Press Q to quit")

if __name__ == "__main__":
    main()