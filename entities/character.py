import math
import pygame

from rect_entity import RectEntity

class Character(RectEntity):
    """Base class for humanoid entities."""
    def __init__(self, x, y, width, height, speed, hp):
        super().__init__(x, y, width, height, speed, hp)

    def get_hurt(self, dmg, character):
        self.hp -= dmg
        if self.hp <= 0:
            character.change_animation('death')
        # Add any additional logic you need when the character gets hurt