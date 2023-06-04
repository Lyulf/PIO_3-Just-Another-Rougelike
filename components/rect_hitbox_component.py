from components.component import *
from enum import Enum

import pygame

class EntityTypes(Enum):
    WALL = 0
    PLAYER = 1
    ENEMY  = 2
    PROJECTILE  = 3

class RectHitboxComponent(Component):
    def __init__(self, rect: pygame.Rect, anchor: pygame.Vector2, entity_type, ignore_types):
        self.rect = rect
        self.anchor = anchor
        self.entity_type = entity_type
        self.ignore_types = ignore_types