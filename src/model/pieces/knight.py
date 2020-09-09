from src.model.pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color, em):
        key_letter = "n"
        super().__init__(color, key_letter, em)
        self.moves = [
            ([1, 2], False),
            ([2, 1], False),
            ([2, -1], False),
            ([-1, 2], False),
            ([1, -2], False),
            ([-1, -2], False),
            ([-2, -1], False),
            ([-2, 1], False)
        ]
