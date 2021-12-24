import os
import random
import time
import os


# screen clear cliche via. popcnt on StackOverflow
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# using a provided screen and a message, create a "text block" that can only be read through the screen.
def from_screen_to_block(screen, message, dist, width=35, height=40):
    # using uppercase messages makes it easier to have the padding characters indistingushable from the message
    message = message.upper()
    flat_block = [-1]*width*height  # create an indicator of what charcters are already filled in
    # inject the message into the block
    for k in range(len(message)):
        flat_block[screen[k]] = message[k] + " "  # an extra space is added for end-user readability.
    # fill in the rest of the message
    for k in range(len(flat_block)):
        if flat_block[k] == -1:  # make sure not to overwrite previous characters (this is the reason for the indicator)
            flat_block[k] = get_random_char(dist) + " "
    return flat_block  # return the list of characters


# create a screen for a new user
def make_screen(width=35, height=40, length=280):
    screen = []  # init a blank screen
    # non-optimized setup, but generates a list of spaces for message characters
    while len(screen) < length:
        possibility = random.randint(0, width*height)  # generate a location
        if possibility not in screen:  # if location isn't already used...
            screen.append(possibility)  # append it to the list
    print(screen)  # debugging
    print(len(screen))  # debugging
    screen.sort()  # sort the screen so the message comes out in a readable order.
    # format the screen into a printable format and return
    return "".join(["  " if k in screen else "# " for k in range(width * height)])


# save a message to a text file so it can be printed
def save_grid(path, data, width=35, height=40):
    # open the file path for writing
    with open(path, "w") as f:
        # write each line
        for _ in range(height):
            f.write("".join(data[:width])+"\n")  # write the first [width] characters to the line
            data = data[width:]  # remove already printed characters


# retrieve a screen
def retrieve_screen(path):
    try:
        with open(path, "r") as f:  # open the file where the screen is stored
            data = "".join(f.readlines())  # extract the data
            print(data)  # print it for debugging
            data = "".join([k for k in data if k != "\n"])  # remove line break characters
            screen = []  # init a blank screen
            for k in range(len(data)//2):  # iterate over data to work on every odd slot
                if data[2*k] == " ":  # if the slot is blank, you can see the char behind it
                    screen.append(k)  # so it's part of the visible area of the screen.
            print(data)
            print(screen)
            print(len(screen))  # debugging
            return screen  # return the result
    except FileNotFoundError:
        return -1  # if the file doesn't exist stop


# get the character distribution
def retrieve_distribution():
    with open("distribution.txt", "r") as f:  # open the distribution file
        dist = [[k[:1], int(k[1:])] for k in f.readlines()]  # turn the data into a dict.
    print(dist)  # debugging
    return dist


# store the character distribution
def save_distribution(dist):
    with open("distribution.txt", "w") as f:
        f.writelines([k[0]+str(k[1])+"\n" for k in dist])  # formatting


# generate a char with a consistent character distribution
def get_random_char(dist):
    pos = random.randint(1, sum([k[1] for k in dist]))  # generate a pointer
    for i in dist:
        if i[1] < pos:
            pos -= i[1]  # of the pointer is ahead of the char, skip and deduct
        else:
            return i[0]  # otherwise return the character
# The principle here is to simulate stuffing a list full of copies of a character and picking one


# the main function. primarily runs the UI.
def main():
    dist = retrieve_distribution()  # grab the distribution
    running = True  # create a quit flag
    while running:  # loop until quit
        # print the option screen
        choice = input("""\n\n\n\n\n---------------
1) write a message
2) create a new screen
3) write to no one
4) Exit

>""")
        if choice == "1":  # "write a message"
            name = input("recipient: ").upper()
            screen = retrieve_screen("screens/"+name)  # get the recipient's name and retrieve their screen
            if screen == -1:
                print("that person doesn't have a screen")
                continue
            message = input("message: ").upper() + "@"  # write a message. @ indicates the message is over
            print(len(message))  # debugging
            if len(message) > 280:
                print("the message is too long.")
                continue  # stop the user if they try to write too long of a message
            for i in range(len(dist)):
                dist[i][1] += len(message.split(dist[i][0])) - 1  # find the count of chars of each type and add to dist
            destination = input("destination: ")
            save_grid(destination, from_screen_to_block(screen, message, dist))  # save the grid to the specified file
            print("grid successfully created.")
        elif choice == "2":  # "create a new screen"
            name = input("Enter the new recipient's name: ").upper()
            screen = make_screen()  # make a screen for the recipient
            save_grid("screens/"+name, screen, 70, 40)  # save the screen to the "screens" folder
            print("Screen successfully created.")
        elif choice == "3":  # "write to no one" (for updating distribution)
            message = input("message: ").upper()
            # update the distribution based on the message
            for i in range(len(dist)):
                split_message = message.split(dist[i][0])
                dist[i][1] += len(split_message) - 1
                message = "".join(split_message)
            while len(message) > 0:
                dist.append([message[0], 0])
                split_message = message.split(dist[-1][0])
                dist[-1][1] += len(split_message) - 1
                message = "".join(split_message)
            print("distribution altered")
        elif choice == "4":  # "exit"
            save_distribution(dist)  # save the data
            running = False  # stop running
        elif choice == "spamton":  # debugging for early code
            os.mkdir("screens")
        else:
            print("that's not a valid input.")


if __name__ == "__main__":
    main()
