import os
import pickle
from _thread import start_new_thread

os.chdir(os.path.join( os.path.dirname(__file__), '../../'))
from src.model.game import Game
from src.em.event_manager import Event_manager

import socket
games = {

}


def threaded_client(conn, addr, idgame, idplayer):
    global games
    game = games[idgame]
    if not game.player_connected():
        return
    while True:
        try:
            data = conn.recv(4096).decode("utf-8")
            print("me pidieron:" + data)
            if not data:
                print("disconnected")
                break
            else:
                if data == "game":
                    reply = pickle.dumps(game)
                    print("mande " + data)
                    conn.sendall(reply)
                elif data == "color":
                    colors = {
                        0: "w",
                        1: "b"
                    }
                    reply = colors[idplayer].encode()
                    conn.sendall(reply)
                elif data != "":
                    game.receive_move(data, idplayer)
                    print("sigo")
                    # conn.sendall("ok".encode("utf-8"))

        except:
            break
    game.player_disconnected()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.0.23", 5010))
s.listen()
n = 0
idgame = 0
while True:
    print("esperando conexiones")
    conn, addr = s.accept()
    print(f"Se conecto: {addr}")
    if n == 0:
        # creo el game
        em = Event_manager(daemon=True)
        games[idgame] = Game(2, 300, em, is_local=False)
        start_new_thread(threaded_client, (conn, addr, idgame, n))
        n += 1
    else:
        start_new_thread(threaded_client, (conn, addr, idgame, n))
        idgame += 1
        n = 0

