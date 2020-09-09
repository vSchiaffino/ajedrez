from src.model.pieces.piece import Piece


class Rook(Piece):
    def __init__(self, color, em):
        key_letter = "r"
        super().__init__(color, key_letter, em)
        self.moves = [
            ([0, 1], True),
            ([1, 0], True),
            ([0, -1], True),
            ([-1, 0], True)
        ]
        self.moved = False
        self.castling = False

    def can_i_castle(self):
        return not self.moved

    def move(self, previous_square, square, chessboard, player_color_turn):
        if self.castling:
            previous_square.set_piece(None)
            square.set_piece(self)
            self.castling = False
            return True
        elif super().move(previous_square, square, chessboard, player_color_turn):
            self.moved = True
            return True
        return False

    def castle(self, actual_square, chessboard, player_color_turn, square_king):
        if actual_square.column == 8: move = -1
        else: move = 1
        next_square = chessboard.get_square_applying_a_move(square_king, [move, 0])
        self.castling = True
        return self.move(actual_square, next_square, chessboard, player_color_turn)


