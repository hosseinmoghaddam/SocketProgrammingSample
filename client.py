import socket
import threading
import re

host = "127.0.0.1"
port = 1550
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
UserGude = ("-exit :exit program\n" +
            "-new$<channel name> :create new channel\n" +
            "-list :channel list\n" +
            "-join$<channel name> :join to channel\n" +
            "-left$<channel name> :left from channel\n" +
            "#<partner name>%massage :Chat by Special user\n")
nick = str(input("welcome, enter your name :"))
print("Hi " + nick + ",\n" + UserGude)


def printMessage():
    msg = str(input(""))
    msg = nick + ":" + msg
    s.send(msg.encode())

while True:
    threading._start_new_thread(printMessage, ())
    data = s.recv(1024)

    print(str(data)[2:-1].replace("^", "\n"))

s.close()
