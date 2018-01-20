import socket
from threading import Thread
import threading

host = "127.0.0.1"
port = 1550
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  # Bind to the port
s.listen(1)
connected = []
chatRoom = []


def isExistUser(data):
    i = 0
    flag = False
    while i < len(connected):
        if data.split("#")[1].split("%")[0] in connected[i]:
            flag = True
            print(i)
            break
        i += 1
    print(i)
    return (flag, i)


def isExistChannel(data):
    i = 0
    flag = False
    while i < len(chatRoom):
        if data.split("$")[1] in chatRoom[i][0]:
            flag = True
            break
        i = i + 1
    return (flag, i)


def isExistChannelM(data):
    i = 0
    flag = False
    j = 1
    while i < len(chatRoom):
        while j < len(chatRoom[i]):
            if data.split(":")[0] in chatRoom[i][j]:
                flag = True
                break
            j += 1
        if flag:
            break
        i = i + 1
    return (flag, i)


def accepter(conn, addr):
    while 1:
        data = str(conn.recv(1024))[2:-1]
        connected.append((data.split(":")[0], conn))
        if data.split(":")[1][0] == "-":
            if data.split(":")[1][:5] == "-exit":  # exit
                print("parted by", addr)
            if data.split(":")[1][:4] == "-new":  # new
                chatRoom.append([data.split("$")[1]])
                chatRoom[len(chatRoom) - 1].append((data.split(":")[0], conn))
                conn.send("created and joined".encode())
                print(chatRoom)
            if data.split(":")[1][:5] == "-list":  # list
                i = 0
                listch = ""
                while i < len(chatRoom):
                    listch = listch + str(i) + "-" + chatRoom[i][0] + "^"
                    i = i + 1
                conn.send(str(listch).encode())
            if data.split(":")[1][:5] == "-join":  # join
                i = 0
                flag = False
                while i < len(chatRoom):
                    if data.split("$")[1] in chatRoom[i][0]:
                        flag = True
                        break
                    i = i + 1
                if flag:
                    chatRoom[i].append((data.split(":")[0], conn))
                    namejoined = "joined " + str(data.split(":")[0]) + " to channel"
                    k = 1
                    while k < len(chatRoom[i]):
                        chatRoom[i][k][1].send(namejoined.encode())
                        k += 1
                    print(chatRoom)
                else:
                    conn.send("channel not found".encode())
            if data.split(":")[1][:5] == "-left":  # left
                flag3, i = isExistChannel(data)
                if flag3:
                    j = 1
                    flag2 = False
                    while j < len(chatRoom[i]):
                        print(chatRoom[i][j])
                        print(data.split(":")[0])
                        if data.split(":")[0] in chatRoom[i][j]:
                            flag2 = True
                            print(i)
                            print(j)
                            print(chatRoom[i][j])
                            break
                        j += 1
                    if flag2:
                        print(i)
                        print(j)
                        namejoined = str(data.split(":")[0]) + " left from channel"
                        k = 1
                        while k < len(chatRoom[i]):
                            chatRoom[i][k][1].send(namejoined.encode())
                            k += 1
                        chatRoom[i].remove(chatRoom[i][j])
                        if len(chatRoom[i]) < 2:
                            chatRoom.remove(chatRoom[i])
                            conn.send(" and remove channel".encode())
                        print(chatRoom)
                    else:
                        conn.send("not joining to channel".encode())

                else:
                    conn.send("not found channel".encode())







        else:
            print(data.split(":")[1][0])
            print(connected)
            if data.split(":")[1][0] == "#":
                (exist, q) = isExistUser(data)
                print((exist, q))

                if exist:
                    connected[q][1].send((data.split("#")[0] + data.split("%")[1]).encode())
                    conn.send((data.split("#")[0] + data.split("%")[1]).encode())

            else:
                j = 1
                (flag3, i) = isExistChannelM(data)
                if flag3:
                    while j < len(chatRoom[i]):
                        print(chatRoom[i][j])
                        print(data.split(":")[0])
                        if data.split(":")[0] in chatRoom[i][j]:
                            k = 1
                            while k < len(chatRoom[i]):
                                chatRoom[i][k][1].send(data.encode())
                                k += 1
                            break
                        j += 1
                else:
                    conn.send(data.encode())

        if not data:
            break
        print(data)


while True:
    print("sever is run")
    conn, addr = s.accept()
    print(connected)
    print("connection by ", addr)
    threading._start_new_thread(accepter, (conn, addr))
