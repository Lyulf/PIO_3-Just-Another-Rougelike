import math
import pygame

from entity import Entitiy

class Character(Entitiy):
    """Base class for humanoid entities."""
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = pygame.Vector2()

    def move(self, dt):
        """Moves the character in time by dt (delta time)."""
        offset = dt * self.speed * self.direction
        self.rect.move_ip(offset.x, offset.y)

    def collide_stage(self, stage_rect):
        """Moves the player back in bounds of the stage."""
        if self.rect.left <= stage_rect.left:
            self.rect.left = stage_rect.left
        elif self.rect.right >= stage_rect.right:
            self.rect.right = stage_rect.right
        if self.rect.top <= stage_rect.top:
            self.rect.top = stage_rect.top
        elif self.rect.bottom >= stage_rect.bottom:
            self.rect.bottom = stage_rect.bottom
