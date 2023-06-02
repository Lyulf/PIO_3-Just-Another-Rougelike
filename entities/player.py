import random
import pygame

from character import Character
from utils.layers import Layers
import ui.spritesheet


class Player(Character):
    """Player character."""
    pygame.init()
    is_loaded = False

    @classmethod
    def load_images(cls):
        if not cls.is_loaded:
            cls.is_loaded = True
            cls.idle_sprite = pygame.image.load("resources/playerModel/idle.png")
            cls.left_sprite = pygame.image.load("resources/playerModel/left.png")
            cls.right_sprite = pygame.image.load("resources/playerModel/right.png")
            cls.down_sprite = pygame.image.load("resources/playerModel/down.png")
            cls.up_sprite = pygame.image.load("resources/playerModel/up.png")

    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)
        self.load_images()
        self.old_color = pygame.Color(246, 187, 148)
        self.new_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.sprite_sheets = {
            'idle' : ui.spritesheet.SpriteSheet(self.idle_sprite, 16, 16, 500, 6, True, self.old_color, self.new_color),
            'left' : ui.spritesheet.SpriteSheet(self.left_sprite, 16, 16, 250, 6, True, self.old_color, self.new_color),
            'right' : ui.spritesheet.SpriteSheet(self.right_sprite, 16, 16, 250, 6, True, self.old_color, self.new_color),
            'down' : ui.spritesheet.SpriteSheet(self.down_sprite, 16, 16, 250, 6, True, self.old_color, self.new_color),
            'up' : ui.spritesheet.SpriteSheet(self.up_sprite, 16, 16, 250, 6, True, self.old_color, self.new_color),
        }
        self.sprite_sheet = self.sprite_sheets['idle']

    def render(self, surface, layer):
        """Renders the player."""
        if layer == Layers.FOREGROUND:

            self.sprite_sheet.animate(surface, self.rect)  # Animate and draw the sprite
            if self.sprite_sheet.is_finished:
                self.sprite_sheet.is_finished = False
                self.sprite_sheet = self.sprite_sheets['idle']

    def change_animation(self, key):
        self.sprite_sheet = self.sprite_sheets[key]
