from time import sleep
import socket
import sys

# Main class module for IRC connection
class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, chan, msg):
        message = "PRIVMSG " + chan + " :" + msg + "\r\n"
        print(message)
        self.irc.send(message.encode())

    def connect(self, server, channel, botnick, password):
        # defines the socket
        print("connecting to:" + server)

        mUser = "USER " + botnick + " " + botnick + " " + botnick + ":DjBaht Activate \r\n"  # user authentication
        mNick = "NICK " + botnick + "\r\n"
        self.mPass = "NickServ IDENTIFY " + password + "\r\n"
        self.mJoin = "JOIN " + channel + "\r\n"

        self.irc.connect((server, 6667))  # connects to the server
        t = self.irc.recv(2040)
        text = t.decode('utf-8')  # receive the text

        self.irc.send(mNick.encode())
        self.irc.send(mUser.encode())

    def get_text(self):

        t = self.irc.recv(2040)
        # receive the text
        text = t.decode('utf-8')

        # Respond to server prompts and Pings with Pongs
        if text.startswith('PING :'):
            print(text)
            mr = 'PONG ' + text.split()[1] + "\r\n"
            mResp = mr.encode()
            print(mResp)
            self.irc.send(mResp)
        elif text.find("If you do not change within 1 minute") != -1:

            # Send password in response for channels that require it
            # This is specifically for irc.snoonet.org, may be different with other servers
            print(text)
            print(self.mPass.encode())
            self.irc.send(self.mPass.encode())
        elif text.find("MODE DjBaht +r") != -1 or text.find("MODE DjBaht +x") != -1:

            # join the channel
            self.irc.send(self.mJoin.encode())
        else:
            print(text)

        return text
