import pygame


class Menu_view:
    def __init__(self, menu):
        # ----- inits ----
        pygame.init()
        pygame.font.init()
        # ---- screen -----
        screen_size = (500, 600)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Chessgame")
        # ----- self attributtes -----
        self.menu = menu
        # ----- colors and images -----
        self.image = pygame.image.load("img/menu_image.jpg")
        self.back_color = pygame.color.Color(41, 128, 185)
        self.button_colors = pygame.color.Color(155, 89, 182)
        self.button_hovered_color = pygame.color.Color(142, 68, 173)
        self.font_color = pygame.color.Color(243, 156, 18)
        # ----- fonts -----
        self.font_label = pygame.font.Font("fonts/roboto.ttf", 23)
        # ----- rects -----
        button_large = (250, 100)
        # ----- first frame -----
        self.image_rect = self.image.get_rect()
        self.one_player_rect = pygame.rect.Rect((125, 225), button_large)
        self.two_player_local_rect = pygame.rect.Rect((125, 350), button_large)
        self.two_player_no_local_rect = pygame.rect.Rect((125, 475), button_large)
        # ----- second frame -----
        # nou

    def get_rects(self):
        return self.one_player_rect, self.two_player_local_rect, self.two_player_no_local_rect

    def get_second_rects(self):
        return self.more_rect, self.less_rect, self.white_rect, self.black_rect

    def refresh_menu(self):
        if not self.menu.type_selected:
            self.refresh_selecting_type()
        else:
            self.refresh_selecting_type()

    def refresh_selecting_type(self):
        # ----- colors -----
        color_1p = self.button_colors
        color_2pl = self.button_colors
        color_2pnl = self.button_colors
        if self.menu.first_hovered:
            color_1p = self.button_hovered_color
        if self.menu.second_hovered:
            color_2pl = self.button_hovered_color
        if self.menu.third_hovered:
            color_2pnl = self.button_hovered_color
        # ----- back -----
        self.screen.fill(self.back_color)
        # ----- image -----
        self.screen.blit(self.image, (100, 25))
        # ---- rects -----
        pygame.draw.rect(self.screen, color_1p, self.one_player_rect)
        pygame.draw.rect(self.screen, color_2pl, self.two_player_local_rect)
        pygame.draw.rect(self.screen, color_2pnl, self.two_player_no_local_rect)
        # ---- fonts -----
        y_offset = 36
        self.screen.blit(self.font_label.render("One player vs computer", 5, self.font_color),
                         (self.one_player_rect.left + 2, self.one_player_rect.top + y_offset))
        self.screen.blit(self.font_label.render("Two players local", 5, self.font_color),
                         (self.two_player_local_rect.left + 36, self.two_player_local_rect.top + y_offset))
        self.screen.blit(self.font_label.render("Two players in network", 5, self.font_color),
                         (self.two_player_no_local_rect.left + 3, self.two_player_no_local_rect.top + y_offset))
        # ----- flip -----
        pygame.display.flip()

    def refresh_time_and_color(self):
        pass
