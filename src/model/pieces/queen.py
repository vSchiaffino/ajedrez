from src.model.pieces.piece import Piece


class Queen(Piece):
    def __init__(self, color, em):
        key_letter = "q"
        super().__init__(color, key_letter, em)
        self.moves = [
            ([0, 1], True),
            ([1, 1], True),
            ([1, 0], True),
            ([1, -1], True),
            ([0, -1], True),
            ([-1, -1], True),
            ([-1, 0], True),
            ([-1, 1], True)
        ]