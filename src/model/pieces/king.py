from src.model.pieces.piece import Piece
import math


class King(Piece):
    def __init__(self, color, em):
        key_letter = "k"
        self.checked = True
        super().__init__(color, key_letter, em)
        self.moves = [
            ([0, 1], False),
            ([1, 1], False),
            ([1, 0], False),
            ([1, -1], False),
            ([0, -1], False),
            ([-1, -1], False),
            ([-1, 0], False),
            ([-1, 1], False)
        ]
        self.special_moves = [
            ([2, 0], False),
            ([-2, 0], False)
        ]
        self.can_do_special_move = True

    def get_possible_moves(self, square, chessboard, player_turn_color):
        moves = super().get_possible_moves(square, chessboard, player_turn_color)
        if player_turn_color == self.color and self.can_do_special_move:
            directions = [-1, 1]
            for direc in directions:
                can = True
                quantity_by_direc = {
                    1: 3,
                    -1: 4
                }
                q = quantity_by_direc[direc]
                rook_square = chessboard.get_square_applying_a_move(square, [q * direc, 0])
                if rook_square.get_piece() is not None and rook_square.can_i_castle():
                    for i in range(1, 3):
                        square_to_move = chessboard.get_square_applying_a_move(square, [direc * i, 0])
                        if square_to_move.get_piece() is not None:
                            can = False
                    if can:
                        moves.append(chessboard.get_square_applying_a_move(square, [direc * 2, 0]))
            return moves
        return moves

    def move(self, previous_square, square, chessboard, player_color_turn):
        if super().move(previous_square, square, chessboard, player_color_turn):
            if math.fabs(previous_square.column - square.column) > 1:
                # is castle i'm gonna check the rook castle
                dif = -(previous_square.column - square.column)
                if dif > 0:
                    q = 3
                else:
                    q = -4
                rook_square = chessboard.get_square_applying_a_move(previous_square, [q, 0])
                r = rook_square.get_piece()
                if r is not None:
                    a = r.castle(rook_square, chessboard, player_color_turn, square)
                    if a:
                        self.can_do_special_move = False
                        return a
            else:
                self.can_do_special_move = False
                return True

        return False

    def check_check(self, square, chessboard):
        self.checked = self.is_checked(square, chessboard)

    def is_checked(self, square, chessboard):
        # ----- horizontal, vertical and diagonal moves -----
        change_color = {
            "w": "b",
            "b": "w"
        }
        dangerous_color = change_color[self.color]
        horizontal_and_vertical_moves = [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1]
        ]
        diagonal_moves = [
            [1, 1],
            [-1, 1],
            [1, -1],
            [-1, -1]
        ]
        dangerous_pieces_1 = [
            "r",
            "q"
        ]
        dangerous_pieces_2 = [
            "b",
            "q"
        ]
        directions = [horizontal_and_vertical_moves, diagonal_moves]
        pieces = [dangerous_pieces_1, dangerous_pieces_2]
        i = 0
        for direc in directions:
            dangerous_pieces = pieces[i]
            for move in direc:
                have_to_break = False
                actual_square = square
                while True:
                    actual_square = chessboard.get_square_applying_a_move(actual_square, move)
                    if actual_square is None or actual_square.get_piece() is not None:
                        have_to_break = True
                    if actual_square is not None and actual_square.do_you_have_this_piece(dangerous_pieces, dangerous_color):
                        return True
                    if have_to_break:
                        break
            i += 1
        # ----- pawns and knights -----
        if self.color == "w":
            moves1 = [
                [1, 1],
                [-1, 1]
            ]
        elif self.color == "b":
            moves1 = [
                [1, -1],
                [-1, -1]
            ]
        moves2 = [
            [2, 1],
            [1, 2],
            [-2, 1],
            [-1, 2],
            [-1, -2],
            [-2, -1],
            [-2, 1],
            [-1, 2]
        ]
        moves3 = [
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
            [0, -1],
            [1, -1]
        ]
        dp1 = "p"
        dp2 = "n"
        dp3 = "k"
        directions = [moves1, moves2, moves3]
        dps = [dp1, dp2, dp3]
        i = 0
        for direc in directions:
            dp = dps[i]
            for move in direc:
                s = chessboard.get_square_applying_a_move(square, move)
                if s is not None and s.do_you_have_this_piece(dp, dangerous_color):
                    return True
            i += 1
        return False





                




