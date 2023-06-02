import pygame
from character import Character
from utils.layers import Layers
import ui.spritesheet


class Opponent(Character):
    """Opponent character."""

    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height, speed)
        self.idle = ui.spritesheet.SpriteSheet("resources/enemies/demon/idle.png", 256, 256, 350, 1, False)
        self.walk = ui.spritesheet.SpriteSheet("resources/enemies/demon/walk.png", 256, 256, 100, 1, False)

        self.hurt = ui.spritesheet.SpriteSheet("resources/enemies/demon/hurt.png", 256, 256, 100, 1, False)
        self.attack = ui.spritesheet.SpriteSheet("resources/enemies/demon/attack.png", 256, 256, 100, 1, False)
        self.death = ui.spritesheet.SpriteSheet("resources/enemies/demon/death.png", 256, 256, 100, 1, False)
        self.sprite_sheet = self.idle

    def render(self, surface, layer):
        """Renders the opponent."""
        if layer == Layers.FOREGROUND:
            pygame.draw.rect(surface, 'yellow', self.rect)
            self.sprite_sheet.animate(surface, self.rect, 35, 70)  # Animate and draw the sprite
            if self.sprite_sheet.is_finished:
                self.sprite_sheet.is_finished = False
                self.sprite_sheet = self.idle

    def change_animation(self, key):
        """TODO later when AI of opponents is added"""
