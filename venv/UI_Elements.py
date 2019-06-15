import pygame


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


class Button:
    def __init__(self, text, color, text_color, location, width, height, action):
        self.text = text
        self.color = color
        self.text_color = text_color
        self.x_pos = location[0]
        self.y_pos = location[1]
        self.width = width
        self.height = height
        self.font_size = 20
        self.button_thickness = 5
        self.action = action

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
