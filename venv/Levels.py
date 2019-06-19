from Frames import Map, Ground
from Objects import Block, Bullet, AbsGameObject
from UI_Elements import LoseMenu, WinMenu, VictoryMenu, Text
from Level_Design_Utilities import time_to_frames
import pygame
import json


class Game:
    def __init__(self, program):
        self.program = program
        self.ball = program.ball
        self.levels = program.levels
        self.window = program.window

    def run(self):
        for level in self.levels:
            result = level.run_level(self.program)

            if result == "win":
                if self.win() == "quit":
                    return "quit"

            if result == "lose":
                return self.lose()

            if result == "quit":
                return "quit"

        return self.victory()

    def lose(self):
        return LoseMenu(self.program).run()

    def win(self):
        return WinMenu(self.program).run()

    def victory(self):
        return VictoryMenu(self.program).run()


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

    def run_level(self, program):
        if Countdown(program, self.level_drag).run() == "quit":
            return "quit"
        ball = program.ball
        frame = 0
        clock = pygame.time.Clock()
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

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


class Countdown:
    #     def __init__(self, text, color, location, font_size):
    #         self.text = text
    #         self.color = color
    #         self.x_pos = location[0]
    #         self.y_pos = location[1]
    #         self.font_size = font_size
    #         self.font = pygame.font.Font(None, self.font_size)
    def __init__(self, program, drag, delay="0:01", count=3, text_color=(255, 255, 255), y_pos=200, font_size=200):
        self.program = program
        self.window = program.window
        self.ball = program.ball
        self.count = count
        self.delay = time_to_frames(delay)
        self.text_color = text_color
        self.y_pos = y_pos
        self.font_size = font_size
        self.draw_list = self.create_draw_list()
        self.center_draw_list()
        self.drag = drag

    def run(self):
        ready_go = 2  # extra messages in addition to the countdown numbers
        frame_counter = 0
        draw_index = 0
        drawing = self.draw_list[draw_index]
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            self.window.refresh()
            drawing.draw(self.window.surface)
            self.ball.draw(self.window.surface)

            # every self.delay frames, the object to be drawn is updated.
            frame_counter += 1
            if frame_counter >= self.delay:
                draw_index += 1
                if draw_index >= self.count + ready_go:
                    return
                frame_counter = 0
                drawing = self.draw_list[draw_index]

            # Let player move ball while waiting
            key_list = pygame.key.get_pressed()
            self.ball.move(key_list, self.drag)

            # Just in case there will be animations in the countdown phase
            AbsGameObject.update_counter()

            pygame.display.update()
            clock.tick(30)

    def create_draw_list(self):
        draw_list = [Text("Ready...", self.text_color, (0, self.y_pos), self.font_size)]
        for num in range(self.count, 0, -1):
            draw_list.append(Text(str(num), self.text_color, (0, self.y_pos), self.font_size))
        draw_list.append(Text("GO!", self.text_color, (0, self.y_pos), self.font_size))
        return draw_list

    def center_draw_list(self):
        for text in self.draw_list:
            text.x_pos = (self.window.width - text.get_width()) // 2

