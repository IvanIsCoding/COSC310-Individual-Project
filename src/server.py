import socket
from sqlite3 import connect
import threading
from hashlib import sha256

# 192.168.1.119
HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
STOP_KEYWORD = sha256("x".encode(FORMAT)).hexdigest()

connections = []


def handle_client(conn: socket, addr):

    print("conn:", conn.getsockname())

    msg = None
    while (msg != STOP_KEYWORD):
        msg = conn.recv(4096).decode(FORMAT)
        index = connections.index((conn, addr))
        if (msg == STOP_KEYWORD):
            connections.remove((conn, addr))
            for connection, _ in connections:
                if len(connections) < 2:
                    connection.send('1 person has left the chat! There is only you left'.encode(FORMAT))
                else:
                    connection.send(f'1 person has left the chat! There are {len(connections)} people left'.encode(FORMAT))

            break

        print(msg)

        if msg:
            print("client ", addr, "says", msg)
            for connection, _ in connections:
                if (connection != conn):
                    connection.send(f'Anonymous: {msg}'.encode(FORMAT))
    print("client", addr, "finished")
    print(conn.getsockname(), "exit")
    conn.close()


# -----------------------main-------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")

while True:
    try:
        conn, addr = s.accept()
        for connection, _ in connections:
            connection.send(
                f'1 person has joined the chat! People in the chat: {len(connections) + 1}'.encode(FORMAT))

        if (conn, addr) not in connections:
            thr = threading.Thread(target=handle_client, args=(conn, addr))
            thr.daemon = False
            thr.start()

            connections.append((conn, addr))
        print(conn)

    except Exception as e:
        print(e)
