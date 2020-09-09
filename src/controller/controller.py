import os
import pygame
import sys

from pydispatch import dispatcher

from src.controller.menu import Menu
from src.view.menu_view import Menu_view

from src.controller.client import Client
from src.model.game import Game
from src.view.view import View
from src.em.event_manager import Event_manager
from src.em.events import Square_clicked, New_game


class Controller:
    def __init__(self):
        """
        Initialize a controller entering into a game main loop.
        """
        # ----- setting self atributtes. -----
        self.y_rect, self.n_rect = "", ""
        time = 300
        # ----- setting the options of the game by the first window loop ----
        type_of_game = self.first_window_loop()
        self.client = None
        self.em = None
        # ----- entering into the game. -----
        if type_of_game == 3:
            # networking things.
            self.game = None
            self.em = None
            players = 2
            self.is_local = False
            self.client = Client()
        else:
            players = type_of_game
            self.is_local = True
            self.em = Event_manager(daemon=True)
            self.game = Game(players, time, self.em, True)
        self.view = View(self.game, self.em, daemon=True, is_local=self.is_local, client=self.client)
        self.square_size = self.view.get_square_size()
        self.game_ended = False
        self.view.start()
        # ----- subscribing to important methods. -----
        dispatcher.send(signal="subscribe", event_name="game_ended", listener=self)
        dispatcher.send(signal="subscribe", event_name="new_game", listener=self)
        # ----- entering to the main loop -----
        self.main_loop()

    def first_window_loop(self):
        players = 0
        local = True
        menu = Menu()
        menu_view = Menu_view(menu)
        first, second, third = menu_view.get_rects()
        while True:
            mouse = pygame.mouse.get_pos()
            menu.first_hovered = first.collidepoint(mouse)
            menu.second_hovered = second.collidepoint(mouse)
            menu.third_hovered = third.collidepoint(mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.first_hovered:
                        return 1
                    if menu.second_hovered:
                        return 2
                    if menu.third_hovered:
                        return 3
            menu_view.refresh_menu()

    def main_loop(self):
        """
        Main loop of the game.
        """
        self.game_ended = False
        while not self.game_ended:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.view.rotate = not self.view.rotate
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.game_ended = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    column = mouse[0] // self.square_size + 1
                    row = mouse[1] // self.square_size + 1
                    if not self.view.rotate:
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
                        row = rotate[row]
                    if not (column < 0 or column > 8 or row < 0 or row > 8):
                        if self.is_local:
                            dispatcher.send(signal="post", event=Square_clicked(row, column))
                        else:
                            num_to_letter = {
                                1: "a",
                                2: "b",
                                3: "c",
                                4: "d",
                                5: "e",
                                6: "f",
                                7: "g",
                                8: "h"
                            }
                            self.client.send_move(num_to_letter[column] + str(row))
        self.decission_loop()

    def decission_loop(self):
        decided = False
        self.y_rect, self.n_rect = self.view.set_decission_screen()
        while not decided:
            mouse = pygame.mouse.get_pos()
            y = self.y_rect.collidepoint(mouse)
            n = self.n_rect.collidepoint(mouse)
            n = True if n == 1 else False
            y = True if y == 1 else False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    decided = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if y:
                        decided = True
                        dispatcher.send(signal='post', event=New_game())
                    if n:
                        decided = True
                        break
            self.view.refresh_decission_screen(y, n)
        pygame.quit()

    # ----------- em method --------------
    def notify(self, event):
        if event.name == "game_ended":
            self.game_ended = True
        if event.name == "new_game":
            self.main_loop()


if __name__ == "__main__":
    controller = Controller()
