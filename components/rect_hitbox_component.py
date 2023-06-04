from components.component import *
from entities.entity_type import *

import pygame

class RectHitboxComponent(Component):
    def __init__(self, rect: pygame.Rect, anchor: pygame.Vector2, entity_type: EntityType, ignore_entity_types: list[EntityType] = None):
        self.rect = rect
        self.anchor = anchor
        self.entity_type = entity_type
        self.ignore_entity_types = ignore_entity_types if ignore_entity_types is not None else []