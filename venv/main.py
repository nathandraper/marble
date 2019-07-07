import pygame
import math
from Frames import Window
from Objects import Ball
from Runnables import MainMenu, TestMenu, Level, VictoryMenu
# TODO: design serious levels
# TODO: more level design utilities
# TODO: endless mode
# TODO: music
# TODO: sound fx
# TODO: improve sprites
# TODO: settings menu
# TODO: rhythm elements
# TODO: change currently running to a stack


class Program:
    def __init__(self):
        pygame.init()
        self.playable_levels = 2
        self.window = self.create_game_window()
        self.ball = self.create_ball(self.window)
        self.run_stack = []

        self.run_stack.append(MainMenu(self))

    def run(self):
        """
        Main run loop for program

        The program runs by popping object off the run stack and running them. The program will run until the run
        stack is empty. Objects are designed to push other objects onto the run stack. Objects include levels
        and menus.
        """
        pygame.init()
        while True:
            try:
                running = self.run_stack.pop()

            except IndexError:
                break

            try:
                running.run()

            except AttributeError:
                break

        pygame.quit()

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


if __name__ == "__main__":
    Program().run()
