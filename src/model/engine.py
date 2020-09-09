import os
import pystockfish


class Engine:
    def __init__(self):
        os.chdir(os.path.join(os.path.dirname(__file__), "../../engine/"))
        self.engine = pystockfish.Engine(depth=20)
        self.position = []
        os.chdir(os.path.join(os.path.dirname(__file__), "../.."))

    def update_pos(self, move):
        self.position.append(move)
        self.engine.setposition(self.position)

    def move(self, game):
        move = self.engine.bestmove()
        game.engine_move(move)
