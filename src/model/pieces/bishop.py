from src.model.pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, color, em):
        key_letter = "b"
        super().__init__(color, key_letter, em)
        # a move is composed of a mov x and mov y and
        # a bool if the movement is linear
        self.moves = [
            ([-1, 1], True),
            ([1, 1], True),
            ([1, -1], True),
            ([-1, -1], True)
        ]
