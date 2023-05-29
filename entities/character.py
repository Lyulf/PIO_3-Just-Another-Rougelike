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
        offset = dt * self.speed * self.direction
        self.rect.move_ip(offset.x, offset.y)
