from components.component import *

import pygame

class TransformComponent(Component):
    def __init__(self, position: pygame.Vector2, rotation: pygame.Vector2, scale: pygame.Vector2):
        self.position = position
        self.rotation = rotation
        self.scale = scale