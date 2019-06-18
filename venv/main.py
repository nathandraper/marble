import pygame
import math
from Frames import Window
from Objects import Ball
from UI_Elements import MainMenu
from Levels import Level, Game
# TODO countdown timer for level start
# TODO design serious levels
# TODO more level design utilities
# TODO endless mode
# TODO music
# TODO improve sprites

class Program:
    def __init__(self):
        pygame.init()
        self.playable_levels = 2
        self.window = self.create_game_window()
        self.ball = self.create_ball(self.window)
        self.levels = None

        self.currently_running = "main_menu"

    def run(self):
        pygame.init()
        while True:
            if self.currently_running == "quit":
                break
            self.currently_running = self.currently_running.run()

        pygame.quit()

    @property
    def currently_running(self):
        return self._currently_running

    @currently_running.setter
    def currently_running(self, obj_name):
        if obj_name == "quit":
            self._currently_running = "quit"
            return

        if obj_name == "level_game":
            # reset ball position
            self.ball.x_pos = (self.window.width // 2) - self.ball.radius
            self.ball.y_pos = self.window.height - 100

            # self.levels needs to be reset each time a game is run because it's a generator object
            self.levels = self.levels_generator(self.playable_levels, self.window)
            self._currently_running = Game(self)
            return

        if obj_name == "main_menu":
            self._currently_running = MainMenu(self)
            return

    @staticmethod
    def create_game_window():
        screen_width = 800
        screen_height = 700
        pygame.display.set_caption("Bullet Marble")
        return Window(screen_width, screen_height)

    @staticmethod
    def create_ball(game_window):
        radius = 10
        x = 500
        y = 500
        ball_color = (10, 90, 109)
        acceleration = 5
        return Ball(game_window.width, game_window.height, ball_color, (x, y), radius, acceleration)

    @staticmethod
    def levels_generator(num, window):
        for x in range(num):
            yield Level("level_" + str(x + 1), window)


if __name__ == "__main__":
    Program().run()
