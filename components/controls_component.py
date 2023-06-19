import pygame

from components.component import *
from enum import Enum
from ui.spritesheet import SpriteSheet
from utils.resources import get_sprite

class Controls(Enum):
    UP = 0,
    LEFT = 1,
    DOWN = 2,
    RIGHT = 3,
    SHOOT = 4,
    USE = 5,


class ControlsComponent(Component):
    def __init__(self, custom_keys: dict, player_color, joystick = None):
        self.custom_keys = custom_keys
        sprite = get_sprite('resources/icons/crosshair.png', True)
        sprite = SpriteSheet.change_color(sprite, pygame.Color('black'), pygame.Color(player_color))
        sprite.set_colorkey('white')
        self.sprite_sheet = SpriteSheet(sprite, 512, 512, 0, 30/512)
        self.crosshair_direction = pygame.Vector2()
        self.joystick = joystick
        self.enabled = False
