class Event:
    """
    Generic event. The events is used to signal differents
    things in the game.
    """
    def __init__(self):
        self.name = "generic_event"


class Square_clicked(Event):
    """
    Event that signal that a square have been clicked. Contains
    the row and the column.
    """
    def __init__(self, row, column):
        """
        Initialize a new square_event.
        :param row: int
        :param column: int
        """
        self.name = "square_clicked"
        self.row = row
        self.column = column


class Game_ended(Event):
    """
    Event signal that the game have been ended. Contains the player that won.
    """
    def __init__(self, player_winner):
        self.name = "game_ended"
        self.player_winner = player_winner


class New_game(Event):
    """
    Event signal that new game has been created.
    """
    def __init__(self):
        self.name = "new_game"
