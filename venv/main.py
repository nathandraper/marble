import pygame
import math
from Frames import Map, Window, Ground
from Sprites import SpriteSheet
from Objects import Ball, Block, AbsGameObject, Bullet
from UI_Elements import Button, Text


# TODO implement these functions
def create_main_menu():
    pass

def create_game_window():
    pass

def create_ball():
    pass


if __name__ == "__main__":
    pygame.init()

    # TODO move all this into the above functions
    screen_width = 800
    screen_height = 700
    game_window = Window(screen_width, screen_height)
    pygame.display.set_caption("Magical Moving Ball")

    test = Ground((400, 400), "platform_texture.png", (2, 5), 5, 5, 5)
    test_button = Button("test", (255, 255, 255), (255, 255, 0), (300, 300), 50, 50)
    test_text = Text("Main Menu", (255, 255, 255), (200, 200), 100)

    game_map = Map([test], screen_width, screen_height, 1)
    test_bullet = Bullet((0,0), "bullet_texture.png", (2, 5), 5, 7*math.pi/4)
    game_map.bullets.append(test_bullet)
    game_map.blocks.append(Block((459, 10), "skull_block.png", (2, 5),  1, 1, 5))

    radius = 10
    x = 500
    y = 500
    ball_color = (10, 90, 109)
    acceleration = 5
    ball = Ball(game_map, screen_width, screen_height, ball_color, (x, y), radius, acceleration)


    clock = pygame.time.Clock()

    run = True
    while run:
        pass


    pygame.quit()
