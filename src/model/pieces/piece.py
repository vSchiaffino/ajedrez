class Piece:
    def __init__(self, color, key_letter, em):
        self.view_key = color + key_letter
        self.key_letter = key_letter
        self.em = em
        self.moves = None
        self.color = color
        self.actually_double_moved = False
        self.checked = False
        # Special move is the one that can be done
        # if is the first move of the piece
        self.can_eat_forward = True
        # eat moves are the once that the condition to move to that square
        # is if a rival piece is in.
        self.eat_moves = []

    def are_you(self, piece, color):
        if isinstance(piece, str):
            return piece == self.key_letter and color == self.color
        elif isinstance(piece, list):
            return True if self.key_letter in piece and self.color == color else False

    def get_possible_moves(self, square, chessboard, player_turn_color):
        """
        Returns the possible moves of a piece.
        :param square: Square
        :param player_turn_color: str
        :param chessboard: Chessboard
        :return: Square[]
        """
        possible_squares = []
        if self.color != player_turn_color:
            return possible_squares
        moves = self.moves

        for move in moves:
            mov = move[0]
            linear = move[1]
            actual_square = square
            if linear:
                piece_or_end_founded = False
                while not piece_or_end_founded:
                    actual_square = chessboard.get_square_applying_a_move(actual_square, mov)
                    if actual_square is None:
                        # it goes to the limit of the board.
                        piece_or_end_founded = True
                    else:
                        if actual_square.get_piece() is None:
                            # square is empty
                            if self.check_if_my_move_affects_the_king(square, actual_square, chessboard):
                                possible_squares.append(actual_square)
                        else:
                            if actual_square.get_color_piece() != self.color:
                                if self.check_if_my_move_affects_the_king(square, actual_square, chessboard):
                                    possible_squares.append(actual_square)
                            piece_or_end_founded = True
            else:
                possible_square = chessboard.get_square_applying_a_move(square, mov)
                # it goes to the board limit ?
                if possible_square is not None:
                    # Is empty or with a rival piece ?
                    # If it's a pawn it can't eat upside.
                    if possible_square.get_piece() is None or (possible_square.get_color_piece() != self.color and
                                                               self.can_eat_forward):
                        # gonna see if the move let's the king in check.
                        if self.check_if_my_move_affects_the_king(square, possible_square, chessboard):
                            possible_squares.append(possible_square)

        return possible_squares

    def check_if_my_move_affects_the_king(self, square, possible_square, chessboard):
        r = False
        king_square = chessboard.king_square[self.color]
        king = king_square.get_piece()
        piece_in_the_possible_square = possible_square.get_piece()
        piece_to_move = self
        possible_square.set_piece(piece_to_move)
        square.set_piece(None)
        if self.key_letter == "k":
            king_square = possible_square
        if not king.is_checked(king_square, chessboard):
            r = True
        square.set_piece(piece_to_move)
        possible_square.set_piece(piece_in_the_possible_square)
        return r

    def can_i_castle(self):
        return False

    def move(self, previous_square, square, chessboard, player_color_turn):
        if square in self.get_possible_moves(previous_square, chessboard, player_color_turn):
            square.set_piece(self)
            previous_square.set_piece(None)
            return True
        return False

    def move_happens(self, piece_moved):
        pass

    # ----------------- getters -----------------
    def piece_is_checked(self):
        return self.checked

    def get_key_letter(self):
        return self.key_letter

    def get_key(self):
        return self.view_key

    def get_color(self):
        return self.color
