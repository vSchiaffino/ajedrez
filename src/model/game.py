from src.model.chessboard import Chessboard
from src.em.events import Game_ended
from pydispatch import dispatcher
from _thread import start_new_thread
from src.model.engine import Engine
import pygame


class Game:
    """
    Chess game.
    """
    # TODO draw
    def __init__(self, players, time_in_seconds, em, is_local=True):
        """
        Initialize a new chess game.
        :param players: int
        :param time_in_seconds: int
        :param em: Event_manager
        """
        # ----- setting self attributes -----
        # game_state[0] is for state of the turn. Can be thinking or moving.
        # game_state[1] is for the player turn. Can be white or black.
        # history is how the pieces moved in the game.
        self.ready = True
        self.is_local = is_local
        self.em = em
        self.color_by_number = {
            0: "white",
            1: "black"
        }
        if players == 1:
            self.vs_machine = True
            # TODO apply this to be choseen by the player
            self.engine = Engine()
            self.engine_number = 1
            self.player_number = 0
        else:
            if not self.is_local:
                self.ready = False
            self.vs_machine = False
        self.players = players
        self.players_on = 0
        self.time_in_seconds = time_in_seconds
        self.game_ended = False
        # ---- subscribing to important events. -----
        dispatcher.send(signal="subscribe", event_name="square_clicked", listener=self)
        dispatcher.send(signal="subscribe", event_name="new_game", listener=self)
        # -----  ------
        # time should be in seconds.
        self.game_state = []
        self.history = []
        self.previous_clicked_square = None
        self.rotate = False
        self.chessboard = Chessboard(self.em)
        self.times = {}
        self.restart_game()

    def player_connected(self):
        if self.players_on < 2:
            self.players_on += 1
            if self.players_on == 2:
                self.ready = True
            return True
        else:
            return False

    def player_disconnected(self):
        self.players_on -= 1
        return self.players_on == 0

    def restart_game(self):
        self.game_state = ["thinking", "white"]
        self.history = []
        self.game_ended = False
        self.previous_clicked_square = None
        self.rotate = False
        self.chessboard = Chessboard(self.em)
        self.times = {
            "white": self.time_in_seconds * 1000,
            "black": self.time_in_seconds * 1000
        }
        start_new_thread(self.time_thread, ())

    def time_thread(self) -> None:
        """
        Threaded function that implements the time mechanic.
        :return: None
        """
        while True:
            if not len(self.history) == 0:
                pygame.time.wait(100)
                self.times[self.game_state[1]] -= 100
                if self.times[self.game_state[1]] == 0:
                    print("Loses: " + self.game_state[1])
                    self.end_game()
                if self.game_ended:
                    break

    def end_game(self):
        """
        Threaded function.
        :return: None
        """
        change_color = {
            "w": "b",
            "b": "w"
        }
        player_lose = self.get_player_color_turn()
        player_win = change_color[player_lose]
        self.game_ended = True
        pygame.time.wait(2)
        dispatcher.send(signal="post", event=Game_ended(player_win))

    def try_to_focus(self, row, column, player) -> None:
        """
        Method that try to set focus to the piece moves.
        :param row: int
        :param column: int
        :param player: int
        :return: None
        """
        if not self.is_local and self.color_by_number[player] != self.game_state[1]:
            return
        self.chessboard.unfocus_all_squares()
        self.previous_clicked_square = self.chessboard.focus_moves(row, column, self.game_state[1][0])
        if self.previous_clicked_square is not None:
            self.change_state()

    def try_to_move(self, row, column, player) -> None:
        """
        Try to move to a specific square.
        :param row: int
        :param column: int
        :param player: int
        :return: None
        """
        move = ""
        if not self.is_local and self.color_by_number[player] != self.game_state[1]:
            return
        if self.chessboard.try_to_move(self.previous_clicked_square, row, column, self.get_player_color_turn()):
            self.change_turn()
            column_number_to_letters = {
                1: "a",
                2: "b",
                3: "c",
                4: "d",
                5: "e",
                6: "f",
                7: "g",
                8: "h"
            }
            new_square = self.chessboard.get_square(row, column)
            prev_square = "{0}{1}".format(column_number_to_letters[self.previous_clicked_square.column],
                                          str(self.previous_clicked_square.row))
            new_square_str = "{0}{1}".format(column_number_to_letters[new_square.column],
                                             str(new_square.row))
            move = prev_square + new_square_str
            self.history.append(move)
            change_color = {
                "w": "b",
                "b": "w",
            }
            if new_square.get_key_letter() == "k":
                self.chessboard.king_square[change_color[self.game_state[1][0]]] = new_square
            # ----- checking check for both kings-----
            keys = ["b", "w"]
            for key in keys:
                king_square = self.chessboard.king_square[key]
                king = king_square.get_piece()
                king.check_check(king_square, self.chessboard)
            self.chessboard.move_happens(new_square.get_piece())
            # ----- checking if the game has ended. -----
            if self.verify_game_ended():
                change_color = {
                    "w": "b",
                    "b": "w"
                }
                player_lose = self.get_player_color_turn()
                player_win = change_color[player_lose]
                print(f"End game. Loses: {player_lose}, wins: {player_win}")
                start_new_thread(self.end_game, ())
        else:
            self.change_state()
        self.chessboard.unfocus_all_squares()
        self.previous_clicked_square = None
        if self.vs_machine:
            self.update_engine(move)

    def engine_move(self, move):
        columns_letters_to_numbers = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8
        }
        move = move["move"]
        square_1 = move[:2]
        square_2 = move[2:4]
        row_1 = int(square_1[1])
        column_1 = columns_letters_to_numbers[square_1[0]]
        row_2 = int(square_2[1])
        column_2 = columns_letters_to_numbers[square_2[0]]
        self.try_to_focus(row_1, column_1, self.engine_number)
        self.try_to_move(row_2, column_2, self.engine_number)

    def receive_move(self, square, player):
        if self.ready:
            print("recibi move: " + square)
            columns_letters_to_numbers = {
                "a": 1,
                "b": 2,
                "c": 3,
                "d": 4,
                "e": 5,
                "f": 6,
                "g": 7,
                "h": 8
            }
            row = int(square[1])
            column = columns_letters_to_numbers[square[0]]
            if self.game_state[0] == "thinking":
                self.try_to_focus(row, column, player)
            else:
                self.try_to_move(row, column, player)


    # --------------------- getters ----------------------
    def get_squares(self) -> list:
        return self.chessboard.get_squares()

    def verify_game_ended(self) -> bool:
        next_turn_color = self.get_player_color_turn()
        for row in self.chessboard.get_squares():
            for square in row:
                if square.get_piece() is not None and square.get_color_piece() == next_turn_color:
                    p_moves = square.get_piece().get_possible_moves(square, self.chessboard, next_turn_color)
                    if len(p_moves) > 0:
                        return False
        return True

    def get_player_color_turn(self) -> str:
        return self.game_state[1][0]

    def get_time(self):
        rs = []
        time_s = [self.times["white"] // 1000, self.times["black"] // 1000]
        for time in time_s:
            m = time // 60
            s = time - m * 60
            m = str(m)
            s = str(s)
            if len(m) == 1:
                m = "0" + m[0]
            if len(s) == 1:
                s = "0" + s[0]
            r = m + ":" + s
            rs.append(r)
        return rs

    def update_engine(self, move):
        if move == "":
            return
        # ----- updating pos -----
        self.engine.update_pos(move)
        if self.color_by_number[self.engine_number] == self.game_state[1]:
            # ---- engine has to move -----
            self.engine.move(self)

    # ----------------- state changing ------------------
    def change_state(self) -> None:
        """
        Changes the state of the game, if the player is thinking,
        change state to moving and if is moving change the state to thinking. 
        """
        state = self.game_state[0]
        change_state = {
            "thinking": "moving",
            "moving": "thinking"
        }
        self.game_state[0] = change_state[state]

    def change_turn(self) -> None:
        """
        Change turns, so if black's moving, now white's moving,
        and vice versa.
        Also switch the state of the turn.
        """
        player = self.game_state[1]
        change_player = {
            "white": "black",
            "black": "white"
        }
        self.game_state[1] = change_player[player]
        # self.rotate = not self.rotate
        self.change_state()

    # ------------------- em method ---------------------
    def notify(self, event) -> None:
        if event.name == 'square_clicked':
            if not self.rotate:
                rotate = {
                    1: 8,
                    2: 7,
                    3: 6,
                    4: 5,
                    5: 4,
                    6: 3,
                    7: 2,
                    8: 1
                }
                event.row = rotate[event.row]
            if self.vs_machine:
                player = self.player_number
            elif self.is_local:
                number_by_color = {
                    "white": 0,
                    "black": 1
                }
                player = number_by_color[self.game_state[1]]
            else:
                # TODO multiplayer network
                pass
            if self.game_state[0] == "thinking":
                self.try_to_focus(event.row, event.column, player)
            else:
                self.try_to_move(event.row, event.column, player)
        if event.name == "new_game":
            self.restart_game()

