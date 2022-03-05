import socket
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
    while (msg != "x"):
        msg = conn.recv(4096).decode(FORMAT)
        if msg == STOP_KEYWORD:
            msg = f'{addr} has left the chat'
            connections.remove(conn)
            conn.send('You have left the chat'.encode(FORMAT))
            conn.close()
        else:
            print("client ", addr, "says", msg)

        for connection, address in connections:
            if (connection != conn):
                connection.send(f'{address}: {msg}'.encode(FORMAT))

    print("client", addr, "finished")
    print(conn.getsockname(), "closed")
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
        
        for connection in connections:
            connection.send(f'{addr} has joined the chat'.encode(FORMAT))
        
        connections.append((conn, addr))
        conn.send('You have joined the chat'.encode(FORMAT))
        print(connections)

        thr = threading.Thread(target=handle_client, args=(conn, addr))
        thr.daemon = False
        thr.start()

    except Exception as e:
        print(e)
