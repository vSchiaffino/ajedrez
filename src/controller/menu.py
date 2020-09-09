class Menu:
    def __init__(self):
        # ----- hovered -----
        self.first_hovered = False
        self.second_hovered = False
        self.third_hovered = False
        # ----- selected -----
        self.selected = 0
        self.type_selected = False
        self.time_choosen = 5
        # ----- color -----
        self.player_color = None
