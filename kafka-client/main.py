# Import Statements
from users import register_user, verify_user

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

def print_welcome_message():
    # Prints Welcome message
    print("Welcome to Kpoll")
    print_options()

def print_options():
    # Prints the avilable options
    print("Please select one of the following options")
    print("Press A to start a poll")
    print("Press S to see results of previous poll")
    print("Press N to register as a new user")
    print("Press V to vote on a poll")
    print("Press Q to quit")

if __name__ == "__main__":
    main()