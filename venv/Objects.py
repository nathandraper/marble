import pygame
from math import floor, hypot, asin, acos, sin, cos, atan, pi, copysign
from Sprites import SpriteSheet


class AbsGameObject:
    flash_counter = 0

    def __init__(self, texture, rows, cols, x_pos, y_pos):
        self.sprite_sheet = SpriteSheet(texture, rows, cols)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def teleport(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self, surface):
        surface.blit(self.sprite_sheet.sheet, (self.x_pos, self.y_pos),
                     self.sprite_sheet.cell_rects[AbsGameObject.flash_counter])


class Ball:
    SQRT2 = 2**.5

    def __init__(self, ball_map, screen_width, screen_height, color, center, radius=1, acceleration=1):
        self.color = color
        self.x_pos = center[0]
        self.y_pos = center[1]
        self.radius = radius
        self.acceleration = acceleration
        self.ball_map = ball_map
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x_velocity = 0
        self.y_velocity = 0
        self.set_rect()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (floor(self.x_pos), floor(self.y_pos)), self.radius)

    def accelerate(self, keys):
        acc = self.acceleration / Ball.SQRT2 if self.is_accelerating_diagonally(keys) else self.acceleration
        self.x_velocity = self.x_velocity + acc * keys[pygame.K_RIGHT] - acc * keys[pygame.K_LEFT]
        self.y_velocity = self.y_velocity + acc * keys[pygame.K_DOWN] - acc * keys[pygame.K_UP]

    def drag(self):
        drag = self.ball_map.drag
        prev_x_vel = self.x_velocity
        prev_y_vel = self.y_velocity

        self.apply_vector(drag,  self.calculate_angle() + pi)

        if (self.x_velocity > 0) != (prev_x_vel > 0):
            self.x_velocity = 0

        if (self.y_velocity > 0) != (prev_y_vel > 0):
            self.y_velocity = 0

    def move(self, keys):
        if self.is_accelerating(keys):
            self.accelerate(keys)
        if self.is_moving():
            self.drag()

        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity

        if self.x_pos > self.screen_width - self.radius:
            self.x_pos = self.screen_width - self.radius
            self.x_velocity = 0
        elif self.x_pos < self.radius:
            self.x_velocity = 0
            self.x_pos = self.radius

        if self.y_pos > self.screen_height - self.radius:
            self.y_pos = self.screen_height - self.radius
            self.y_velocity = 0
        elif self.y_pos < self.radius:
            self.y_velocity = 0
            self.y_pos = self.radius
        self.set_rect()

        if self.is_blocked():
            self.blocked()

        if self.is_off_the_grid():
            self.off_the_grid()

    def is_accelerating(self, keys):
        return any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN]])

    def is_moving(self):
        return (self.x_velocity != 0) or (self.y_velocity != 0)

    def is_accelerating_diagonally(self, keys):
        return (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and (keys[pygame.K_UP] or keys[pygame.K_DOWN])

    def is_blocked(self):
        return self.rect.collidelist(self.ball_map.get_block_rects()) >= 0

    def is_off_the_grid(self):
        return self.rect.collidelist(self.ball_map.get_platform_rects()) < 0

    def blocked(self):
        print("collide")

    def off_the_grid(self):
        print("off da grid")

    def teleport(self, center):
        self.x_pos = center[0]
        self.y_pos = center[1]
        self.set_rect()

    def set_rect(self):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.radius*2, self.radius*2)

    def calculate_velocity(self):
        return hypot(self.x_velocity, self.y_velocity)

    def calculate_angle(self):
        if self.x_velocity == 0:
            return copysign(pi/2, self.y_velocity)
        var = atan((-1 * self.y_velocity)/self.x_velocity)
        return var

    def apply_vector(self, magnitude, angle):
        y_component = sin(angle) * magnitude
        x_component = cos(angle) * magnitude

        self.y_velocity -= y_component
        self.x_velocity += x_component


class Block(AbsGameObject):
    def __init__(self, location, texture, rows_cols, width, height, velocity):
        super().__init__(texture, rows_cols[0], rows_cols[1], location[0], location[1])
        self.width = width
        self.height = height
        self.velocity = velocity
        self.flash_counter = 0
        self.set_rect()


    def fall(self):
        self.y_pos += self.velocity
        self.set_rect()

    def set_rect(self):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.sprite_sheet.cell_width, self.sprite_sheet.cell_height)


class Boost(AbsGameObject):
    def __init__(self, location, orientation, acceleration = 50):
        self.orientation = orientation
        icon = pygame.transform.scale(pygame.image.load("boost_" + str(orientation) + ".png"), (30, 30))
        super().__init__(location[0], location[1], icon)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        if orientation not in ["left", "right", "up", "down"]:
            raise OrientationError(orientation)
        else:
            self._orientation = orientation