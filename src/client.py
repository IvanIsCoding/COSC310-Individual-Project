import socket
from hashlib import sha256

FORMAT = "utf8"

STOP_KEYWORD = sha256("x".encode(FORMAT)).hexdigest()


class Client:
    def __init__(self, host="127.0.0.1", port=65432):
        try:
            self.host = host
            self.port = port
            self.connect()
        except Exception as e:
            print(e)
            exit(1)

    def connect(self) -> None:
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print('client address', self.sock.getsockname())

    def receive_message(self) -> str:
        return self.sock.recv(4096).decode(FORMAT)

    def send_message(self, msg) -> None:
        self.sock.send(msg.encode(FORMAT, 'backslashreplace'))
