import pygame
import threading
from pydispatch import dispatcher
from _thread import start_new_thread


class View(threading.Thread):
    def __init__(self, game, em, daemon, is_local=True, client=None):
        # ----- threading init -----
        super().__init__(daemon=daemon)
        threading.Thread.__init__(self)
        # ----- pygame init -----
        icon = pygame.image.load("img/wp.png")
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Chessgame")
        pygame.display.set_icon(icon)
        # ----- self attributes -----
        self.client = client
        self.is_local = is_local
        self.backcolor = ""
        self.yes_rect = ""
        self.yes_color = ""
        self.yes_resalted_color = ""
        self.no_rect = ""
        self.no_color = ""
        self.no_resalted_color = ""
        self.square_size = 75
        self.screen_size = (0, 0)
        self.screen = ""
        self.set_game_screen()
        self.game = game
        self.em = em
        self.rotate = False
        self.blit = True
        self.color = self.client.get_color()
        # ----- pieces -----
        piece_size = (75, 75)
        self.pieces = {
            "br": pygame.transform.scale(pygame.image.load("img/br.png"), piece_size),
            "bn": pygame.transform.scale(pygame.image.load("img/bn.png"), piece_size),
            "bb": pygame.transform.scale(pygame.image.load("img/bb.png"), piece_size),
            "bk": pygame.transform.scale(pygame.image.load("img/bk.png"), piece_size),
            "bq": pygame.transform.scale(pygame.image.load("img/bq.png"), piece_size),
            "bp": pygame.transform.scale(pygame.image.load("img/bp.png"), piece_size),
            "wr": pygame.transform.scale(pygame.image.load("img/wr.png"), piece_size),
            "wn": pygame.transform.scale(pygame.image.load("img/wn.png"), piece_size),
            "wb": pygame.transform.scale(pygame.image.load("img/wb.png"), piece_size),
            "wk": pygame.transform.scale(pygame.image.load("img/wk.png"), piece_size),
            "wq": pygame.transform.scale(pygame.image.load("img/wq.png"), piece_size),
            "wp": pygame.transform.scale(pygame.image.load("img/wp.png"), piece_size)
        }
        # ----- font -----
        self.font = pygame.font.Font("fonts/roboto.ttf", 60)
        self.font_label = pygame.font.Font("fonts/roboto.ttf", 60)
        # ----- colors -----
        self.colors = {
            "black": pygame.color.Color(118, 150, 86),
            "white": pygame.color.Color(238, 238, 210),
            "red": pygame.color.Color(243, 62, 66)
        }
        self.focus_color = pygame.color.Color(81, 209, 246)
        # ----- subscribing to important events. -----
        if self.is_local:
            dispatcher.send(signal="subscribe", event_name="game_ended", listener=self)
            dispatcher.send(signal="subscribe", event_name="new_game", listener=self)

    def set_game_screen(self):
        self.blit = True
        self.screen_size = (750, 600)
        self.screen = pygame.display.set_mode(self.screen_size)

    def refresh(self):
        if not self.is_local:
            game = self.client.get_game()
        else:
            game = self.game
        # ----- Squares and pieces -----
        for row in game.get_squares():
            for square in row:
                # ----- square blitzing -----
                color = self.colors[square.get_square_color()]
                row = square.get_row() - 1
                column = square.get_column() - 1
                pos = (column * self.square_size, row * self.square_size)
                if not self.rotate:
                    pos = (pos[0], self.screen_size[1] - self.square_size - pos[1])
                middle_pos = (pos[0] + self.square_size // 2, pos[1] + self.square_size // 2)
                rect = pygame.Rect(pos, (self.square_size, self.square_size))
                pygame.draw.rect(self.screen, color, rect)
                # ----- pieces blitzing -----
                piece_y_offset = 0
                piece_x_offset = 0
                piece = square.get_piece()
                if piece is not None:
                    if piece.get_key()[1] == "p":  # The pawns have a different offset idk why
                        piece_y_offset = -3
                    self.screen.blit(self.pieces[piece.get_key()], (pos[0] + piece_x_offset, pos[1] + piece_y_offset))
                # ----- focus blitzing -----
                focus = square.get_focus()[0]
                color = square.get_focus()[1]
                if focus:
                    if self.is_local or color == self.color:
                        pygame.draw.circle(self.screen, self.focus_color, middle_pos, 10, 0)
                    # print(f"[DEBUG] {square.row}, {square.column} IS FOCUSED")
        # ----- time blitzing -----
        # containers
        color = pygame.color.Color(255, 255, 255)
        for i in (0, 7):
            for j in (8, 9):
                pos = (j * self.square_size, i * self.square_size)
                rect = pygame.Rect(pos, (self.square_size, self.square_size))
                pygame.draw.rect(self.screen, color, rect)
        # letters
        cs = [7, 0]
        i = 0
        for c in cs:
            lx_offset = 0
            ly_offset = 5
            times = game.get_time()
            pos = (8 * self.square_size + lx_offset, c * self.square_size + ly_offset)
            p1 = times[i]
            w = pygame.color.Color(0, 0, 0)
            self.screen.blit(self.font.render(str(p1), 5, w), pos)
            i += 1
        # ----- blitzing terminated -----
        pygame.display.flip()

    def set_decission_screen(self):
        self.font_label = pygame.font.Font("fonts/roboto.ttf", 40)
        self.blit = False
        self.screen_size = (500, 300)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.backcolor = pygame.color.Color(52, 152, 219)
        pos_y = 100
        large_x = 200
        large_y = 150
        self.yes_rect = pygame.rect.Rect(33, pos_y, large_x, large_y)
        self.yes_color = pygame.color.Color(39, 174, 96)
        self.yes_resalted_color = pygame.color.Color(46, 204, 113)
        self.no_rect = pygame.rect.Rect(267, pos_y, large_x, large_y)
        self.no_color = pygame.color.Color(192, 57, 43)
        self.no_resalted_color = pygame.color.Color(231, 76, 60)
        return self.yes_rect, self.no_rect

    def refresh_decission_screen(self, y, n):
        # ----- rects -----
        color_y = self.yes_color
        color_n = self.no_color
        if y:
            color_y = self.yes_resalted_color
        if n:
            color_n = self.no_resalted_color
        self.screen.fill(self.backcolor)
        pygame.draw.rect(self.screen, color_y, self.yes_rect)
        pygame.draw.rect(self.screen, color_n, self.no_rect)
        # ----- labels -----
        label_color = pygame.color.Color(241, 196, 15)
        self.screen.blit(self.font_label.render("Do you wanna play again?", 5, label_color), (25, 30))
        self.screen.blit(self.font_label.render("Play again", 5, label_color), (39, 150))
        self.screen.blit(self.font_label.render("Exit", 5, label_color), (335, 150))
        pygame.display.flip()

# -------------- getters --------------
    def get_square_size(self):
        return self.square_size

# -------------- function of threading that is always looping --------------
    def run(self):
        # print("run")
        while self.blit:
            print("blitzed")
            self.refresh()

# -------------- em method -------------------
    def notify(self, event):
        if event.name == "game_ended":
            self.set_decission_screen()
        elif event.name == "new_game":
            self.set_game_screen()
            start_new_thread(self.run, ())
