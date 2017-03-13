from baht import *
import os
import random

# The bot takes commands by users sending the channel a message starting with '*'
# followed by any of the listed commands.
# Example: '*help' will pull up help and the list of predefined bot commands


def comm_test(x):
    if x.startswith("*"):
        xlen = len(x.split(" "))

        # For commands that split into an array of 2 or 3 spaces
        if xlen == 2 or xlen == 1:
            return True
        else:
            return False
    else:
        return False


def get_response(y, z):

    useragent = z
    print(useragent)
    ylen = len(y.split(" "))

    # Check if command is pointed at an irc user
    if ylen == 2:
        user = y.split(" ")[1]
    else:
        user = ""

    commands = {
        "dj": ["wat",
               "%s... I swear..." % useragent,
               ],
        "foo": ["bar", "baz", "boop"],
        "help": ['All commands (starting with \'*\' to signal the bot): '
                 '*h4x USERNAME: Send this command for DjBaht to "hack" another irc user'
                 '*mug USERNAME: Send this command for DjBaht to "mug" another irc user']
    }

    user_commands = {
        # To send ACTION commands the string needs to be escaped with "\001" in order for irc to respond
        "h4x": ["\001ACTION h4x %s\'s mainframe.\001" % user,
                "\001ACTION plants a worm on %s\'s computer that plays \"Kidz Bop 33\" on infinite loop\001" % user,
                "\001ACTION plants a worm on %s\'s computer that plays Nickelback on infinite loop\001" % user,
                "\001ACTION dumps a metric crap-ton of Malware on %s\'s HD\001" % user,
                "\001ACTION changes %s\'s desktop wallpaper\001" % user,
                "sudo rm -rf /... fuuu",
                "%s: it has begun..." % useragent,
                "\'Operation Cupcake\' was successful",
                ],
        "mug": ["\001ACTION bites %s\'s nose off then steals their checkbook\001" % user,
                "\001ACTION hits %s across the face with sock full of quarters then takes their wallet\001" % user,
                ]
    }

    if ylen == 1:
        for c in commands:
            print(c, y)
            if y == c:
                irc.send(channel, random.choice(commands[c]))
                break
    elif ylen == 2:
        ucomm = y.split(" ")[0]

        for c in user_commands:
            print(c, ucomm)
            if ucomm == c:
                irc.send(channel, random.choice(user_commands[c]))
                break


def main():

    while 1:
        text = irc.get_text()

        # Command for termination, send via PM
        if master in text and "PRIVMSG DjBaht :djbaht_kill" in text:
            print("DjBaht Terminated")
            sys.exit()

        # Check for DjBaht commands
        elif "PRIVMSG " in text and channel in text:

            print("Elif works")
            comm = text.split("PRIVMSG " + channel + " :")[1].strip()
            print(comm)

            # Parsing and editing the response string for commands
            if comm_test(comm):
                comm = comm.split("*")[1]
                # u = text.split("/")[1]
                # u = u.split(" ")[0]
                u = text.split(":")[1]
                u = u.split("!")[0]
                get_response(comm, u)


if __name__ == '__main__':
    channel = input("Enter the channel you would like to connect to (e.g. '#python'): ")
    server = input("Enter the server name: ")
    nickname = input("Enter your bots nick name: ")

    # Depending on server/channel password may be omitted or may need reconfigured
    # this works with irc.snoonet.org, I cannot speak for others
    password = input("Enter your bots password: ")

    # The "master" is allowed to terminate the bot via PM message
    master = input("Enter the nick of the user who controls the bot: ")
    irc = IRC()
    irc.connect(server, channel, nickname, password)
    main()
