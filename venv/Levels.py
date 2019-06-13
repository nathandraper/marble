from Frames import Map, Ground
from Objects import Block
from Sprites import SpriteSheet
import pygame


class Level:
    # TODO implement this level base class
    def __init__(self, aMap, aGround):
        self.map = aMap
        self.ground = aGround

# TODO design levels as JSON data with platform data and time intervals as objects
# TODO implement win/lose conditions
