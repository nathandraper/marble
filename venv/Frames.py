import pygame
from Sprites import SpriteSheet


class Map:
    def __init__(self, platform, screen_width, screen_height, has_platform=False):
        self.blocks = []
        self.bullets = []
        self.platform = platform
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.has_platform = has_platform

    def update(self, surface):
        self.bullets_shoot()
        self.blocks_fall()
        self.draw(surface)

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

        for ground in self.platform:
            ground.draw(surface)

        for bullet in self.bullets:
            bullet.draw(surface)

    def blocks_fall(self):
        for index, block in enumerate(self.blocks):
            block.fall()
            if block.is_offscreen(self.screen_width, self.screen_height):
                self.blocks.pop(index)

    def bullets_shoot(self):
        for index, bullet in enumerate(self.bullets):
            bullet.shoot()
            if bullet.is_offscreen(self.screen_width, self.screen_height):
                self.bullets.pop(index)

    def get_block_rects(self):
        return[block.rect for block in self.blocks]

    def get_platform_rects(self):
        try:
            return[ground.rect for ground in self.platform]
        except TypeError:
            return[pygame.Rect(0, 0, self.screen_width, self.screen_height)]

    def get_bullet_rects(self):
        return[bullet.rect for bullet in self.bullets]

    def on_what_ground(self, rect):
        return rect.collidelist(self.get_platform_rects)


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height))

    def refresh(self):
        self.surface.fill((0, 0, 0))


class Ground:
    def __init__(self, location, texture, rows_cols, width, height, drag):
        self.texture_sheet = SpriteSheet(texture, rows_cols[0], rows_cols[1])
        self.drag = drag
        self.animation_frames = rows_cols[0] * rows_cols[1]
        self.flash_counter = 0
        self.x_pos = location[0]
        self.y_pos = location[1]
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width * self.texture_sheet.cell_width, self.height * self.texture_sheet.cell_height)

    def draw(self, surface):
        for row in range(self.height):
            for col in range(self.width):

                surface.blit(self.texture_sheet.sheet, (self.x_pos + col * self.texture_sheet.cell_width,
                                                        self.y_pos + row * self.texture_sheet.cell_height),
                             self.texture_sheet.cell_rects[self.flash_counter])
        if self.flash_counter >= self.animation_frames - 1:
            self.flash_counter = 0
        else:
            self.flash_counter += 1
