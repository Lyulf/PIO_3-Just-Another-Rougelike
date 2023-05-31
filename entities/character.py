import math
import pygame

from rect_entity import RectEntity

class Character(RectEntity):
    """Base class for humanoid entities."""
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)