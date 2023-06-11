import pygame

from components.interaction_component import *
from ui.rect_area import *

class InteractableArea(InteractionComponent):
    def __init__(self, rect: pygame.Rect, anchor: pygame.Vector2, interaction, color, line_offset: pygame.Vector2 = None, line_spacing: pygame.Vector2 = None):
        super().__init__(rect, anchor, interaction)
        self.area = RectArea(rect, color, line_offset=line_offset, line_spacing=line_spacing)

    def draw(self, surface: pygame.Surface, position: pygame.Vector2):
        self.area.draw(surface, position - self.anchor)
