import pygame


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
                    return "quit"
                if event.type == pygame.KEYUP:
                    if keys[pygame.K_t] and keys[pygame.K_LCTRL]:
                        return "test_menu"
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True

            if click:
                for button in self.buttons:
                    if button.in_button(pygame.mouse.get_pos()):
                        return button.obj
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
                             self.button_height, "quit")
        play_button = Button("Play", self.button_color, self.text_color, self.play_button_location, self.button_width,
                             self.button_height, "level_game")
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
                                 self.button_width, self.button_height, "continue")
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
                             self.button_height, "quit")
        mainmenu_button = Button("main menu", self.button_color, self.text_color, self.mainmenu_button_location,
                                 self.button_width, self.button_height, "main_menu")
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
                                 self.button_width, self.button_height, "main_menu")
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
