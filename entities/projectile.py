import pygame
from utils.layers import Layers
from rect_entity import RectEntity

class Projectile(RectEntity):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x,y,width,height,speed)

    def render(self, surface, layer):
        """Renders the projectile."""
        if layer == Layers.FOREGROUND:
            # Should be replaced with character sprite in the future
            pygame.draw.rect(surface, 'green', self.rect)