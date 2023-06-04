from components.component import *

import pygame

class RectSpriteComponent(Component):
    def __init__(self, rect: pygame.Rect, anchor: pygame.Vector2, color: str):
        self.rect = rect
        self.anchor = anchor
        self.color = color
