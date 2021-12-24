import os
import random
import time


# def from_block_to_screen(flat_block, message):
#     print("After")
#     block_list = [[k] for k in range(len(flat_block)) if flat_block[k] == message[0]]
#     for char in message[1:]:
#         new_block_list = []
#         print(len(block_list))
#         for chain in block_list:
#             new_block_list += [(chain + [k]) for k in range(chain[-1]+1, len(flat_block)) if flat_block[k] == char]
#         block_list = new_block_list
#     if len(block_list) == 0:
#         print("Message doesn't fit ;(")
#         return False
#     chosen = random.choice(block_list)
#     print(message)
#     print(chosen)
#     print("".join([flat_block[k] for k in chosen]))


# def from_block_to_screen(flat_block, message):
#     chain = []
#     barrier = 0
#     while True:
#         for char in message:
#             pool = [k for k in range(barrier, len(flat_block)) if flat_block[k] == char]
#             if len(pool) == 0:
#                 break
#             chain.append(random.choice(pool))
#             barrier = chain[-1] + 1
#         if len(message) > len(chain):
#             continue
#         print(message)
#         print(chain)
#         print("".join([flat_block[k] for k in chain]))


# def make_block(dist, height=40, width=35):
#     block = []
#     for _ in range(height):
#         line = ""
#         for _ in range(width):
#             line += get_random_char(dist) + " "
#         block.append(line)
#     print("\n".join(block))
#     return block


def from_screen_to_block(screen, message, dist, width=35, height=40):
    message = message.upper()
    flat_block = [-1]*width*height
    for k in range(len(message)):
        flat_block[screen[k]] = message[k] + " "
    for k in range(len(flat_block)):
        if flat_block[k] == -1:
            flat_block[k] = get_random_char(dist) + " "

    return flat_block
    # block_clip = flat_block
    # block = []
    # for _ in range(height):
    #     block.append("".join(block_clip[:width]))
    #     block_clip = block_clip[width:]
    # print("\n".join(block))
    # print("".join(["".join(block)[2*k] for k in screen]))


def make_screen(width=35, height=40, length=280):
    screen = []
    while len(screen) < length:
        possibility = random.randint(0, width*height)
        if possibility not in screen:
            screen.append(possibility)
    print(screen)
    print(len(screen))
    screen.sort()
    return "".join(["  " if k in screen else "# " for k in range(width * height)])


def save_grid(path, data, width=35, height=40):
    with open(path, "w") as f:
        for _ in range(height):
            f.write("".join(data[:width])+"\n")
            data = data[width:]


def retrieve_screen(path):
    try:
        with open(path, "r") as f:
            data = "".join(f.readlines())
            print(data)
            data = "".join([k for k in data if k != "\n"])
            screen = []
            for k in range(len(data)//2):
                if data[2*k] == " ":
                    screen.append(k)
            print(data)
            print(screen)
            print(len(screen))
            return screen
    except FileNotFoundError:
        return -1


def retrieve_distribution():
    with open("distribution.txt", "r") as f:
        dist = [[k[:1], int(k[1:])] for k in f.readlines()]
    print(dist)
    return dist


def save_distribution(dist):
    with open("distribution.txt", "w") as f:
        f.writelines([k[0]+str(k[1])+"\n" for k in dist])


def get_random_char(dist):
    pos = random.randint(1, sum([k[1] for k in dist]))
    for i in dist:
        if i[1] < pos:
            pos -= i[1]
        else:
            return i[0]


def main():
    dist = retrieve_distribution()
    running = True
    while running:
        choice = input("""\n\n\n\n\n---------------
1) write a message
2) create a new screen
3) write to no one
4) Exit

>""")
        if choice == "1":
            name = input("recipient: ").upper()
            screen = retrieve_screen("screens\\"+name)
            if screen == -1:
                print("that person doesn't have a screen")
                continue
            message = input("message: ").upper() + "@"
            print(len(message))
            if len(message) > 280:
                print("the message is too long.")
                continue
            for i in range(len(dist)):
                dist[i][1] += len(message.split(dist[i][0])) - 1
            destination = input("destination: ")
            save_grid(destination, from_screen_to_block(screen, message, dist))
            print("grid successfully created.")
        elif choice == "2":
            name = input("Enter the new name: ").upper()
            screen = make_screen()
            save_grid("screens\\"+name, screen, 70, 40)
            print("Screen successfully created.")
        elif choice == "3":
            message = input("message: ").upper()
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
        elif choice == "4":
            save_distribution(dist)
            running = False
        elif choice == "spamton":
            os.mkdir("screens")
        else:
            print("that's not a valid input.")


if __name__ == "__main__":
    main()


# start_dist = retrieve_distribution()
# extract("screen.txt")
# from_screen_to_block(extract("screen.txt"), "HELLO, SANDRA. PLEASE APPEAR AT THE PACIFIC VIEW MALL ON THE FIRST OF MARCH. YOU WILL BE TASKED WITH COVERTLY MAKING SURE THAT TROY IS WITHOUT HIS SPOON. GOOD LUCK, - GARIBALDI", start_dist)
# from_block_to_screen("".join(make_block("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'\":;.!? @)),TAKE THIS MESSAGE TO TRENT")
