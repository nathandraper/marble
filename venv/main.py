import pygame
import math
from Frames import Map, Window, Ground
from Sprites import SpriteSheet
from Objects import Ball, Block, AbsGameObject, Bullet
from UI_Elements import Button, Text, Menu
from Levels import Level, Game


def run_main_menu(window):
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

    main_menu = Menu([play_button, quit_button], [message], window)

    return main_menu.run_menu()


def create_game_window():
    screen_width = 800
    screen_height = 700
    pygame.display.set_caption("Bullet Marble")
    return Window(screen_width, screen_height)


def create_ball(game_window):
    radius = 10
    x = 500
    y = 500
    ball_color = (10, 90, 109)
    acceleration = 5
    return Ball(game_window.width, game_window.height, ball_color, (x, y), radius, acceleration)


def levels_generator(num, window):
    for x in range(num):
        yield Level("level_" + str(x + 1), window)


if __name__ == "__main__":
    pygame.init()
    playable_levels = 1

    game_window = create_game_window()
    ball = create_ball(game_window)

    while True:
        choice = run_main_menu(game_window)
        if choice == "quit":
            break
        if choice == "play":
            Game(ball, levels_generator(playable_levels, game_window), game_window).run_levels()

    pygame.quit()
