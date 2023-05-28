import pygame

from character import Character
from utils.layers import Layers

class Player(Character):
    """Player character."""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def render(self, surface, layer):
        """Renders the player."""
        if layer == Layers.FOREGROUND:
            # Should be replaced with character sprite in the future
            pygame.draw.rect(surface, 'red', self.rect)
        
