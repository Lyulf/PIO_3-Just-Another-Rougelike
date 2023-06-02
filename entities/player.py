import random
import pygame

from character import Character
from utils.layers import Layers
import ui.spritesheet


class Player(Character):
    """Player character."""

    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)
        self.old_color = pygame.Color(246, 187, 148)
        self.new_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.idle = ui.spritesheet.SpriteSheet("resources/playerModel/idle.png", 16, 16, 500, 6, True, self.old_color, self.new_color)
        self.left = ui.spritesheet.SpriteSheet("resources/playerModel/left.png", 16, 16, 250, 6, True, self.old_color, self.new_color)
        self.right = ui.spritesheet.SpriteSheet("resources/playerModel/right.png", 16, 16, 250, 6, True, self.old_color, self.new_color)
        self.down = ui.spritesheet.SpriteSheet("resources/playerModel/down.png", 16, 16, 250, 6, True, self.old_color, self.new_color)
        self.up = ui.spritesheet.SpriteSheet("resources/playerModel/up.png", 16, 16, 250, 6, True, self.old_color, self.new_color)
        self.sprite_sheet = self.idle

    def render(self, surface, layer):
        """Renders the player."""
        if layer == Layers.FOREGROUND:
            pygame.draw.rect(surface, 'red', self.rect)  # Draw the red rectangle first

            self.sprite_sheet.animate(surface, self.rect)  # Animate and draw the sprite
            if self.sprite_sheet.is_finished:
                self.sprite_sheet.is_finished = False
                self.sprite_sheet = self.idle

    def change_animation(self, key):
        if key == 'right':
            self.sprite_sheet = self.right
        if key == 'left':
            self.sprite_sheet = self.left
        if key == 'up':
            self.sprite_sheet = self.up
        if key == 'down':
            self.sprite_sheet = self.down



