import pygame

from components.component import *

class InteractionComponent(Component):
    def __init__(self, rect: pygame.Rect, anchor: pygame.Vector2, interaction):
        self.rect = rect
        self.anchor = anchor
        self.interaction = interaction
