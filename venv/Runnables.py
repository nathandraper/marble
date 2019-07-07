from Frames import Map, Ground
from Objects import Block, Bullet, AbsGameObject
from Level_Design_Utilities import time_to_frames
import pygame
import json

class LevelGame:
    def __init__(self, run_stack, num_levels, window):
        self.run_stack = run_stack
        self.num_levels = num_levels
        self.window = window

    def run(self):
        self.run_stack.append(VictoryMenu(self))
        for i in range(self.num_levels, 0, -1):
            self.run_stack.append(Level(f"level_{i}", self.window))


class Level:
    def __init__(self, jason, window, program):
        self.program = program
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

    def run(self):
        if Countdown(self.program, self.level_drag).run() is None:
            return
        ball = self.program.ball
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
                    self.program.run_stack.append(WinMenu(self.program))
                    return
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

            if ball.is_shot(self.level_map) or ball.is_blocked(self.level_map):
                program.run_stack.append(LoseMenu(self.program))
                return

            if self.level_map.has_platform:
                if ball.is_off_the_grid(self.level_map):
                    program.run_stack.append(LoseMenu(self.program))

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
                    program.run_stack.append(None)
                    return None

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


class Menu:
    def __init__(self, program):
        # default styling
        self.button_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.button_width = 100
        self.button_height = 100
        self.font_size = 30
        self.button_space = 50

        # other properties
        self.buttons = []
        self.texts = []
        self.program = program
        self.window = self.program.window

    def draw(self):
        self.window.surface.fill((0, 0, 0))

        for button in self.buttons:
            button.draw(self.window.surface)
        for text in self.texts:
            text.draw(self.window.surface)

        pygame.display.update()

    def run(self):
        self.draw()
        clock = pygame.time.Clock()

        run = True
        click = False
        while run:
            keys = pygame.key.get_pressed()



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.program.run_stack.append(None)
                    return
                if event.type == pygame.KEYUP:
                    if keys[pygame.K_t] and keys[pygame.K_LCTRL]:
                        return "test_menu"
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True

            if click:
                for button in self.buttons:
                    if button.in_button(pygame.mouse.get_pos()):
                        button.push(self.program.run_stack)
                        return
            clock.tick(60)

    def center_elements(self):
        for text in self.texts:
            text.x_pos = (self.window.width - text.get_width()) // 2

        buttons_width = sum([button.width + self.button_space for button in self.buttons]) - self.button_space
        last_button = 0
        for button in self.buttons:
            button.x_pos = last_button + (self.window.width - buttons_width) // 2
            last_button += button.width + self.button_space

    def create_buttons(self):
        # TODO implement general button creation method
        pass

    def create_texts(self):
        return [Text(self.message, self.text_color, self.text_location, self.font_size)]


class TestMenu(Menu):
    def __init__(self, program):
        # get default styling values
        super().__init__(program)

        # text parameters
        self.message = "Testing"
        self.text_location = (0,200)

        # button parameters
        self.test_1_location = self.main_menu_location = (0,400)

        # create buttons and text
        self.buttons.extend(self.create_buttons())
        self.texts.extend(self.create_texts())

        self.center_elements()

    def create_buttons(self):
        test_button1 = Button("Test level 1", self.button_color, self.text_color, self.test_1_location,
                              self.button_width, self.button_height, "test_1")
        mainmenu_button = Button("Main Menu", self.button_color, self.text_color, self.main_menu_location,
                                 self.button_width, self.button_height, "main_menu")

        return [test_button1, mainmenu_button]


class MainMenu(Menu):
    def __init__(self, program):
        # get default styling values
        super().__init__(program)

        # button parameters
        self.play_button_location = self.quit_button_location = (0, 400)

        # text parameters
        self.message = "Bullet Marble"
        self.text_location = (0, 200)

        # create buttons and text
        self.buttons.extend(self.create_buttons())
        self.texts.extend(self.create_texts())

        self.center_elements()

    def create_buttons(self):
        quit_button = Button("Quit", self.button_color, self.text_color, self.quit_button_location, self.button_width,
                             self.button_height, None)
        play_button = Button("Play", self.button_color, self.text_color, self.play_button_location, self.button_width,
                             self.button_height, LevelGame(self.program.run_stack, self.program.playable_levels,
                                                           self.program.window))
        return [play_button, quit_button]


class WinMenu(Menu):
    def __init__(self, program):
        # get default styling values
        super().__init__(program)

        # button parameters
        self.continue_button_location = (0, 400)

        # text parameters
        self.message = "Level complete!"
        self.text_location = (0, 200)

        # create buttons and text
        self.buttons.extend(self.create_buttons())
        self.texts.extend(self.create_texts())

        self.center_elements()

    def create_buttons(self):
        continue_button = Button("Continue", self.button_color, self.text_color, self.continue_button_location,
                                 self.button_width, self.button_height, [])
        return [continue_button]


class LoseMenu(Menu):
    def __init__(self, program):
        # get default styling values
        super().__init__(program)

        # button parameters
        self.mainmenu_button_location = self.quit_button_location = (0, 400)

        # text parameters
        self.message = "Failure!"
        self.text_location = (0, 200)

        # create buttons and text
        self.buttons.extend(self.create_buttons())
        self.texts.extend(self.create_texts())

        self.center_elements()

    def create_buttons(self):
        quit_button = Button("Quit", self.button_color, self.text_color, self.quit_button_location, self.button_width,
                             self.button_height, None)
        mainmenu_button = Button("main menu", self.button_color, self.text_color, self.mainmenu_button_location,
                                 self.button_width, self.button_height, MainMenu(self.program))
        return [mainmenu_button, quit_button]


class VictoryMenu(Menu):
    def __init__(self, program):
        # get default styling values
        super().__init__(program)

        # button parameters
        self.mainmenu_button_location = (0, 400)

        # text parameters
        self.message = "You beat the game!"
        self.text_location = (0, 200)

        # create buttons and text
        self.buttons.extend(self.create_buttons())
        self.texts.extend(self.create_texts())

        self.center_elements()

    def create_buttons(self):
        mainmenu_button = Button("main menu", self.button_color, self.text_color, self.mainmenu_button_location,
                                 self.button_width, self.button_height, MainMenu(self.program))
        return [mainmenu_button]


class Button:
    def __init__(self, text, color, text_color, location, width, height, obj):
        self.text = text
        self.color = color
        self.text_color = text_color
        self.x_pos = location[0]
        self.y_pos = location[1]
        self.width = width
        self.height = height
        self.font_size = 20
        self.button_thickness = 5
        self.obj = obj

        self.font = pygame.font.Font(None, self.font_size)

    def draw(self, surface):
        message = self.font.render(self.text, True, self.text_color)
        rect = (self.x_pos, self.y_pos, self.width, self.height)
        text_x = self.x_pos + (self.width - message.get_width()) // 2
        text_y = self.y_pos + (self.height - message.get_height()) // 2

        pygame.draw.rect(surface, self.color, rect, self.button_thickness)
        surface.blit(message, (text_x, text_y))

    def in_button(self, coordinates):
        return (self.x_pos < coordinates[0] < self.x_pos + self.width) and (
                self.y_pos < coordinates[1] < self.y_pos + self.height)

    def push(self, run_stack):
        if self.obj == []:
            return

        run_stack.append(self.obj)


class Text:
    def __init__(self, text, color, location, font_size):
        self.text = text
        self.color = color
        self.x_pos = location[0]
        self.y_pos = location[1]
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)

    def draw(self, surface):
        message = self.font.render(self.text, True, self.color)
        surface.blit(message, (self.x_pos, self.y_pos))

    def get_width(self):
        return self.font.size(self.text)[0]