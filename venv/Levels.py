from Frames import Map, Ground
from Objects import Block
from Sprites import SpriteSheet
import pygame


class Level:
    def __init__(self, aMap, aGround):
        self.map = aMap
        self.ground = aGround
