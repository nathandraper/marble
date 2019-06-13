import pygame
import math
from Frames import Map, Window, Ground
from Sprites import SpriteSheet
from Objects import Ball, Block, AbsGameObject, Bullet

# TODO clean up this mess
# TODO create game main menu
if __name__ == "__main__":
    pygame.init()

    screen_width = 800
    screen_height = 700
    game_window = Window(screen_width, screen_height)
    pygame.display.set_caption("Magical Moving Ball")

    test = Ground((400, 400), "platform_texture.png", (2, 5), 5, 5, 5)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game_window.refresh()
        key_list = pygame.key.get_pressed()
        ball.move(key_list)
        game_map.draw(game_window.surface)
        ball.draw(game_window.surface)
        game_map.blocks_fall()
        game_map.bullets_shoot()
        pygame.display.update()

        if AbsGameObject.flash_counter >= 9:
            AbsGameObject.flash_counter = 0
        else:
            AbsGameObject.flash_counter += 1
        clock.tick(30)

    pygame.quit()
