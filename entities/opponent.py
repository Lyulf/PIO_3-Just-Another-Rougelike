import pygame
from character import Character
from utils.layers import Layers

class Opponent(Character):
    """Opponent character."""
    def __init__(self, x, y, width, height,speed):
        super().__init__(x, y, width, height,speed)

    def render(self, surface, layer):
        """Renders the opponent."""
        if layer == Layers.FOREGROUND:
            pygame.draw.rect(surface, 'yellow', self.rect)