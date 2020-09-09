from src.model.pieces.piece import Piece
import math


def can_move_to(square):
    return square.get_piece() is None


class Pawn(Piece):
    def __init__(self, color, em):
        key_letter = "p"
        super().__init__(color, key_letter, em)
        move_modifier_by_color = {
            "w": 1,
            "b": -1
        }
        self.can_eat_forward = False
        move_modifier = move_modifier_by_color[color]
        self.move_modifier = move_modifier
        self.moves = [
            ([0, 1 * move_modifier], False)
        ]
        self.special_move = [0, 1 * move_modifier]
        self.eat_moves = [
            [1, move_modifier],
            [-1, move_modifier]
        ]
        self.can_do_special_move = True

    def move(self, previous_square, square, chessboard, player_color_turn):
        # ---- gonna check if the move is en passant -----
        ste = None
        is_passant_move = False
        if previous_square.column != square.column:
            # is an eat move.
            if square.get_piece() is None:
                # en passant
                move_modifier_by_color = {
                    "w": -1,
                    "b": 1
                }
                ste = chessboard.get_square_applying_a_move(square, [0, move_modifier_by_color[self.color]])
                is_passant_move = True
        ans = super().move(previous_square, square, chessboard, player_color_turn)
        if ans:
            if is_passant_move:
                ste.set_piece(None)
                is_passant_move = False
                ste = None
            if self.actually_double_moved:
                self.actually_double_moved = False
            if math.fabs(previous_square.row - square.row) == 2:
                self.actually_double_moved = True
            self.can_do_special_move = False
        return ans

    def get_possible_moves(self, square, chessboard, player_turn_color):
        moves = super().get_possible_moves(square, chessboard, player_turn_color)
        if self.color == player_turn_color:
            # ----- double move -----
            if self.can_do_special_move and \
                    chessboard.get_square_applying_a_move(square, (0, self.move_modifier)).get_piece() is None:
                square_1 = chessboard.get_square_applying_a_move(square, (0, self.move_modifier * 2))
                if can_move_to(square_1) and self.check_if_my_move_affects_the_king(square, square_1, chessboard):
                    moves.append(square_1)
            # ----- eating moves -----
            for e_move in self.eat_moves:
                square_e = chessboard.get_square_applying_a_move(square, e_move)
                if square_e is not None and square_e.get_piece() is not None and \
                        square_e.get_color_piece() != self.get_color() and \
                        self.check_if_my_move_affects_the_king(square, square_e, chessboard):
                    moves.append(square_e)
            # ----- en passant move -----
            row_by_color = {
                "w": 5,
                "b": 4
            }
            move_modifier_by_color = {
                "w": 1,
                "b": -1
            }
            if row_by_color[self.color] == square.row:
                possible_pawns = ([1, 0], [-1, 0])
                for possible_pawn in possible_pawns:
                    s = chessboard.get_square_applying_a_move(square, possible_pawn)
                    if s is not None and s.get_piece() is not None and s.get_piece().actually_double_moved:
                        move = chessboard.get_square_applying_a_move(square, [possible_pawn[0],
                                                                              move_modifier_by_color[self.color]])
                        if self.check_if_my_move_affects_the_king(square, move, chessboard):
                            moves.append(move)
            # ----- ready -----
        return moves

    def move_happens(self, piece_moved):
        if not self == piece_moved:
            self.actually_double_moved = False
