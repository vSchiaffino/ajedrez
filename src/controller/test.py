import socket
from client import Client

c = Client()
i = 0
while True:
    game = c.get_game()
    print("tengo el game")
    if i % 10 == 0:
        c.send_move("e2")

    i += 1

