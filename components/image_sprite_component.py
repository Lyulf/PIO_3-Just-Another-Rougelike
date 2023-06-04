from components.component import *
from ui.spritesheet import SpriteSheet

import pygame

class ImageSpriteComponent(Component):
    def __init__(self, rect: pygame.Rect, anchor: pygame.Vector2, sprite_sheets: dict[SpriteSheet], sprite_sheet_key: str, offset: pygame.Vector2 = None):
        self.rect = rect
        self.anchor = anchor
        self.sprite_sheets = sprite_sheets
        self.current_sprite = self.sprite_sheets[sprite_sheet_key]
        self.offset = offset if offset is not None else pygame.Vector2()