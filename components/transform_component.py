from components.component import *

import pygame

class TransformComponent(Component):
    def __init__(self, position: pygame.Vector2 = None, rotation: pygame.Vector2 = 0, scale: pygame.Vector2 = None):
        self.position = position if position is not None else pygame.Vector2()
        self.rotation = rotation
        self.scale = scale if scale is not None else pygame.Vector2(1, 1)

    def projection(self, camera_transform):
        position = self.position - camera_transform.position
        rotation = self.rotation + camera_transform.rotation
        scale = self.scale * camera_transform.scale
        result = TransformComponent(
            position=position,
            rotation=rotation,
            scale=scale,
        )
        return result