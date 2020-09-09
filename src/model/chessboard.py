from src.model.square import Square
from src.model.pieces.pawn import Pawn
from src.model.pieces.rook import Rook
from src.model.pieces.queen import Queen
from src.model.pieces.king import King
from src.model.pieces.bishop import Bishop
from src.model.pieces.knight import Knight


class Chessboard:
    """
    Represents the board in a chess game. It's a array of
    squares.
    """

    def __init__(self, em):
        """
        Initialize a new chessboard.
        """
        # ----- setting self attributes -----
        self.em = em
        # ----- initializing the squares -----
        self.squares = []
        for r in range(8):
            row = []
            for c in range(8):
                color = ((r + 1) + (c + 1)) % 2
                aux = {
                    0: "black",
                    1: "white"
                }
                color = aux[color]
                row.append(Square(r + 1, c + 1, color, self.em))
            self.squares.append(row)
        self.king_square = {
            "w": self.get_square(1, 5),
            "b": self.get_square(8, 5)
        }
        # ----- initializing the pieces -----
        self.put_pieces()

    def move_happens(self, piece_moved):
        for row in self.squares:
            for s in row:
                s.move_happens(piece_moved)

    def put_pieces(self):
        """
        This function puts the pieces in the right form.
        """
        # ---- pawns ----
        color_by_row = {
            2: "w",
            7: "b"
        }
        for r in (2, 7):
            color = color_by_row[r]
            for c in range(1, 9):
                self.get_square(r, c).set_piece(Pawn(color, self.em))
        # ---- all other pieces ----
        pieces_by_column = {
            1: Rook,
            2: Knight,
            3: Bishop,
            4: Queen,
            5: King,
            6: Bishop,
            7: Knight,
            8: Rook
        }
        color_by_row = {
            1: "w",
            8: "b"
        }
        for r in (1, 8):
            color = color_by_row[r]
            for c in range(1, 9):
                self.get_square(r, c).set_piece(pieces_by_column[c](color, self.em))

    def unfocus_all_squares(self):
        """
        Set the focus off in all squares.
        """
        for row in self.squares:
            for square in row:
                square.unfocus()

    def focus_moves(self, row, column, player_turn_color):
        return self.get_square(row, column).focus_piece_moves(player_turn_color, self)

    def try_to_move(self, previous_square, row, column, player_color_turn):
        new_square = self.get_square(row, column)
        return previous_square.piece.move(previous_square, new_square, self, player_color_turn)

    # --------------------- getters ----------------------
    def get_squares(self):
        return self.squares

    def get_square_applying_a_move(self, square, mov):
        """
        Returns a new square after applying a specific mov in the square given.
        :param square: Square
        :param mov: int[]
        :return: Square
        """
        return self.get_square(square.row + mov[1], square.column + mov[0])

    def get_square(self, row, column):
        """
        Returns the square in the specific row or column.
        If a invalid row is given, returns None.
        :param row: int
        :param column: int
        :return: Square or None
        """
        if row >= 9 or column >= 9 or column <= 0 or row <= 0:
            return None
        return self.squares[row - 1][column - 1]

    # --------------------- setters ----------------------

    # ------------------- em notify --------------------
    def notify(self, event):
        pass
