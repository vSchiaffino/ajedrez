import socket
import pickle


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("192.168.0.23", 5010))

    def get_game(self):
        self.s.sendall("game".encode("utf-8"))
        data = self.s.recv(4096 * 3)
        game = pickle.loads(data)
        return game

    def send_move(self, move):
        data = move.encode("utf-8")
        self.s.sendall(data)
        # if self.s.recv(4096).decode("utf-8") == "ok":
        #     print("ok")

    def get_color(self):
        self.s.sendall("color".encode("utf-8"))
        color = self.s.recv(4096).decode()
        return color
