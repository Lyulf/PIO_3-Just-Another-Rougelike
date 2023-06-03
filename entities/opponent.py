import pygame
from character import Character
from utils.layers import Layers
import ui.spritesheet


class Opponent(Character):
    """Opponent character."""
    pygame.init()
    is_loaded = False
    @classmethod
    def load_images(cls):
        if not cls.is_loaded:
            cls.is_loaded = True
            cls.idle_sprite = pygame.image.load("resources/enemies/demon/idle.png")
            cls.walk_sprite = pygame.image.load("resources/enemies/demon/walk.png")
            cls.hurt_sprite = pygame.image.load("resources/enemies/demon/hurt.png")
            cls.attack_sprite = pygame.image.load("resources/enemies/demon/attack.png")
            cls.death_sprite = pygame.image.load("resources/enemies/demon/death.png")

    def __init__(self, x, y, width, height, speed, hp):
        super().__init__(x, y, width, height, speed, hp)
        self.load_images()
        self.sprite_sheets = {
            'idle' : ui.spritesheet.SpriteSheet(self.idle_sprite, 256, 256, 350, 1, False),
            'walk' : ui.spritesheet.SpriteSheet(self.walk_sprite, 256, 256, 100, 1, False),
            'hurt' : ui.spritesheet.SpriteSheet(self.hurt_sprite, 256, 256, 1000, 1, False),
            'attack' : ui.spritesheet.SpriteSheet(self.attack_sprite, 256, 256, 100, 1, False),
            'death' : ui.spritesheet.SpriteSheet(self.death_sprite, 256, 256, 100, 1, False),
        }
        self.sprite_sheet = self.sprite_sheets['idle']

    def render(self, surface, layer):
        """Renders the opponent."""
        if layer == Layers.FOREGROUND:
            self.sprite_sheet.animate(surface, self.rect, 35, 70)  # Animate and draw the sprite
            if self.sprite_sheet.is_finished:
                if self.sprite_sheet == self.sprite_sheets['death']:
                    self.hp = -1
                self.sprite_sheet.is_finished = False
                self.sprite_sheet = self.sprite_sheets['idle']

    def change_animation(self, key):
        self.sprite_sheet = self.sprite_sheets[key]