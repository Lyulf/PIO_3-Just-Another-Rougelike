import pygame

from entity import Entitiy

class Character(Entitiy):
    """Base class for humanoid entities."""

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
