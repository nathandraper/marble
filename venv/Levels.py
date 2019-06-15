from Frames import Map, Ground
from Objects import Block, Bullet, AbsGameObject, Ball
from Sprites import SpriteSheet
from UI_Elements import Button, Text, Menu
import pygame
import json


class Game:
    def __init__(self, ball, levels, window):
        self.ball = ball
        self.levels = levels
        self.window = window

    def run_levels(self):
        for level in self.levels:
            result = level.run_level(self.ball)

            if result == "win":
                self.win()

            if result == "lose":
                return self.lose()

        return self.victory()

    def lose(self):
        color = (0, 255, 255)
        text_color = (255, 255, 255)
        main_menu_location = (300, 600)
        width = 100
        height = 50

        main_menu_button = Button("Main Menu", color, text_color, main_menu_location, width, height, "main menu")
        message_font = pygame.font.Font(None, 30)
        message = message_font.render("You Lose!", True, text_color)

        menu = Menu([main_menu_button], [message], self.window)
        return menu.run_menu()

    def win(self):
        color = (0, 255, 255)
        text_color = (255, 255, 255)
        location = (450, 600)
        width = 100
        height = 50

        continue_button = Button("Continue", color, text_color, location, width, height, "")
        message_font = pygame.font.Font(None, 30)
        message = message_font.render("Level complete!", True, text_color)

        menu = Menu([continue_button], [message], self.window)

        return menu.run_menu()

    def victory(self):
        color = (0, 255, 255)
        text_color = (255, 255, 255)
        location = (450, 600)
        width = 100
        height = 50

        continue_button = Button("Main Menu", color, text_color, location, width, height, "main_menu")
        message_font = pygame.font.Font(None, 30)
        message = message_font.render("You beat the game!", True, text_color)

        menu = Menu([continue_button], [message], self.window)

        return menu.run_menu()


class Level:
    def __init__(self, jason, window):
        self.jason = jason
        self.window = window
        self.screen_width = window.width
        self.screen_height = window.height
        self.level_data = self.read_json()
        self.level_map = self.load_map(self.level_data["map"])
        self.level_drag = self.level_data["drag"]

    def read_json(self):
        with open(self.jason, 'r') as data:
            return json.load(data)

    def load_map(self, data):
        if not data["platform_enabled"]:
            return Map([], self.screen_width, self.screen_height)

        level_map = Map([], self.screen_width, self.screen_height, True)
        for ground in data["platform"]:
            level_map.platform.append(ground["texture"], ground["rows_cols"],
                                      ground["width"], ground["width"], ground["drag"])
        return level_map

    def run_level(self, ball):
        frame = 0
        clock = pygame.time.Clock()
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.window.refresh()
            key_list = pygame.key.get_pressed()

            if str(frame) in self.level_data:
                if self.level_data[str(frame)] == "win":
                    return "win"
                if "bullets" in self.level_data[str(frame)]:
                    self.level_map.bullets.extend([Bullet(*x) for x in self.level_data[str(frame)]["bullets"]])

                if "blocks" in self.level_data[str(frame)]:
                    self.level_map.blocks.extend([Block(*x) for x in self.level_data[str(frame)]["blocks"]])

            if self.level_map.has_platform:
                drag = self.level_map.platform[self.level_map.on_what_ground(ball.rect())]
            else:
                drag = self.level_drag

            ball.move(key_list, drag)
            self.level_map.update(self.window.surface)
            ball.draw(self.window.surface)

            if ball.is_shot(self.level_map):
                return "lose"

            if ball.is_blocked(self.level_map):
                return "lose"

            if self.level_map.has_platform:
                if ball.is_off_the_grid(self.level_map):
                    return "lose"

            AbsGameObject.update_counter()

            pygame.display.update()
            frame += 1
            clock.tick(30)


