class Square:
    """
    Represents a square in the chessboard.
    """
    def __init__(self, row, column, square_color, em):
        """
        Form a new square for the chessboard.
        
        row -- Int for the row. With subscript 1.
        column -- Int for the column. With subscript 1.
        square_color -- Must be a string: "black" or "white"
        """
        # ----- setting self attributes. -----
        self.color_focused = None
        self.piece = None
        self.row = row
        self.column = column
        self.square_color = square_color
        self.em = em
        self.focused = False

    def can_i_castle(self):
        """
        Ask to the piece(if haves), if the king can castle in that direction.

        :return: bool
        """
        if self.get_piece() is None or not self.piece.can_i_castle():
            return False
        else:
            return True

    def focus_piece_moves(self, player_turn_color, chessboard):
        """
        Method that applies the focus to the possible moves of the
        piece in the square. And returns if the game_state must be changed.
        :param player_turn_color: str
        :param chessboard: Chessboard
        :return: bool
        """
        if self.piece is None:
            return None
        possible_squares = self.piece.get_possible_moves(self, chessboard, player_turn_color)
        if len(possible_squares) <= 0:
            return None
        for square in possible_squares:
            square.focus(player_turn_color)
        return self

    def do_you_have_this_piece(self, piece, color):
        return self.piece.are_you(piece, color) if self.piece is not None else False

    def move_happens(self, piece_moved):
        if self.get_piece() is not None:
            self.piece.move_happens(piece_moved)

# --------------------- getters ----------------------
    def get_square_color(self):
        return self.square_color if self.get_piece() is None or not self.piece.piece_is_checked() else "red"

    def get_key_letter(self) -> str:
        return self.piece.get_key_letter()

    def get_focus(self):
        return [self.focused, self.color_focused]

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_piece(self):
        return self.piece

    def get_color_piece(self):
        if self.piece is None:
            return None
        return self.piece.get_color()

# --------------------- setters ----------------------
    def set_piece(self, piece):
        if self.piece is not None:
            pass
        self.piece = piece

    def focus(self, color_piece):
        self.color_focused = color_piece
        self.focused = True

    def unfocus(self):
        self.color_focused = None
        self.focused = False
