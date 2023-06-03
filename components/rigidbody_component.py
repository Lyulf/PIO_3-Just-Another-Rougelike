from components.component import *
from enum import Enum

import pygame

class CollisionType(Enum):
    NONE = 0
    STATIC = 1
    KINETIC = 2
    DYNAMIC = 3

class RigidbodyComponent(Component):
    def __init__(self, speed: pygame.Vector2, collision_type: CollisionType = CollisionType.DYNAMIC, direction: pygame.Vector2 = None):
        self.speed = speed
        self.direction = direction if direction is not None else pygame.Vector2()
        self.collision_type = collision_type