import pygame
import math
from Frames import Window
from Objects import Ball
from UI_Elements import MainMenu
from Levels import Level, Game


class Program:
    def __init__(self):
        pygame.init()
        self.playable_levels = 1
        self.window = self.create_game_window()
        self.ball = self.create_ball(self.window)
        self.levels = None

        self.currently_running = MainMenu(self)

    def run(self):
        pygame.init()
        while True:
            if self.currently_running == "quit":
                break

            run_this = self.currently_running.run()
            self.set_currently_running(run_this)

        pygame.quit()

    def set_currently_running(self, obj_name):
        if obj_name == "quit":
            self.currently_running = "quit"
            return

        if obj_name == "level_game":
            self.levels = self.levels_generator(self.playable_levels, self.window)
            self.currently_running = Game(self)
            return

        if obj_name == "main_menu":
            self.currently_running = MainMenu(self)
            return

    @staticmethod
    def create_main_menu(window):
        color = (255, 255, 255)
        text_color = (255, 255, 255)
        quit_button_location = (600, 500)
        play_button_location = (300, 500)
        width = 100
        height = 100

        quit_button = Button("Quit", color, text_color, quit_button_location, width, height, "quit")
        play_button = Button("Play", color, text_color, play_button_location, width, height, "play")

        text_location = (150, 200)
        font_size = 30

        message = Text("Bullet Marble", text_color, text_location, font_size)

        return Menu([play_button, quit_button], [message], window)

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
