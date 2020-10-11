
def main():
    print_welcome_message()
    cmd = ""
    off = False
    while not off:
        cmd = input()
        if cmd == "Q":
            print("Thank-you")
            off = True
        else:
            print("Invalid Option")
            print_options()


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