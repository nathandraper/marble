from Frames import Map, Ground
from Objects import Block, Bullet, AbsGameObject, Ball
from Sprites import SpriteSheet
from UI_Elements import Button, Text
import pygame
import json


class Menu:
    def __init__(self, buttons, texts, window):
        self.buttons = buttons
        self.texts = texts
        self.window = window

    def render(self):
        for button in buttons:
            button.draw(window.surface)

        self.description.draw(window.surface)

    def run_menu(self):
        for button in self.buttons:
            button.draw()
        for text in self.texts:
            text.draw()

        run = True
        while run:
            if pygame.mouse.get_pressed()[0]:
                for button in self.buttons:
                    if button.in_button(pygame.mouse.get_pos()):
                        return button.action


class Game:
    def __init__(self, ball, levels, window):
        self.ball = ball
        self.levels = levels
        self.window = window

    def run_levels(self):
        for level in levels:
            if level.run_level() == "win":
                self.win()

            if level.run_level() == "lose":
                return self.lose()

        return self.victory()

    def lose(self):
        color = (0, 255, 255)
        text_color = (255, 255, 255)
        retry_location = (600, 600)
        main_menu_location = (300, 600)
        width = 100
        height = 50

        retry_button = Button("Retry", color, text_color, retry_location, width, height, "retry")
        main_menu_button = Button("Main Menu", color, text_color, main_menu_location, width, height, "main menu")
        message_font = pygame.font.Font(None, 30)
        message = message_font.render("You Lose!", True, text_color)

        menu = Menu([main_menu_button, retry_button], [message], self.window)
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


# TODO Design levels
class Level:
    def __init__(self, game, jason):
        self.game = game
        self.jason = jason
        self.level_data = self.read_json()
        # TODO make function to read ground/platform data from JSON and create map
        self.level_map = self.level_data["map"]

    def read_json(self):
        with open(self.jason, 'r') as data:
            return json.load(data)

    def run_level(self, game, ball, window):
        frame = 0
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.window.surface.refresh()
            key_list = pygame.key.get_pressed()

            if frame in self.level_data:
                if self.level_data[frame] == "win":
                    return "win"
                if "bullets" in self.level_data[frame]:
                   self.bullets.extend(self.level_data[frame]["bullets"])

                if "blocks" in self.level[frame]:
                    self.blocks.extend(self.level_data[frame]["blocks"])

            self.ball.move(key_list)
            self.level_map.update()
            self.ball.draw(window.surface)

            if ball.is_shot:
                return "lose"

            if ball.is_blocked:
                return "lose"

            if ball.is_off_the_grid:
                return "lose"

            AbsGameObject.update_counter()

            pygame.display.update()
            frame += 1
            clock.tick(30)


