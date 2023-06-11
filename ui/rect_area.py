import pygame
import math

class RectArea(object):
    def __init__(self, rect: pygame.Rect, color, offset: pygame.Vector2 = None, line_offset: pygame.Vector2 = None, line_spacing: pygame.Vector2 = None, font = None):
        self.rect = rect
        self.color = color
        self.offset = offset if offset is not None else pygame.Vector2()
        self.line_offset = line_offset if line_offset is not None else pygame.Vector2(0, 20)
        self.line_spacing = line_spacing if line_spacing is not None else pygame.Vector2(0, 5)
        self.font = font if font is not None else pygame.font.Font('resources/mainMenu/font.ttf', 28)
        self.rect_surface = self.__pre_draw()

    def __pre_draw(self):
        rect_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        #rect_surface.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.rect(rect_surface, self.color, self.rect, 3)
        try:
            i = -1
            while True:
                start_pos = self.rect.topleft + i * self.line_spacing
                end_pos = self.rect.topright + i * self.line_spacing + self.line_offset
                start_pos, end_pos = self.rect.clipline(start_pos, end_pos)
                pygame.draw.line(rect_surface, self.color, start_pos, end_pos, 2)
                i -= 1
        except ValueError:
            pass

        try:
            i = 0
            while True:
                start_pos = self.rect.topleft + i * self.line_spacing
                end_pos = self.rect.topright + i * self.line_spacing + self.line_offset
                start_pos, end_pos = self.rect.clipline(start_pos, end_pos)
                pygame.draw.line(rect_surface, self.color, start_pos, end_pos, 2)
                i += 1
        except ValueError:
            pass

        try:
            i = -1
            while True:
                start_pos = self.rect.topleft + i * self.line_spacing + self.line_offset
                end_pos = self.rect.topright + i * self.line_spacing
                start_pos, end_pos = self.rect.clipline(start_pos, end_pos)
                pygame.draw.line(rect_surface, self.color, start_pos, end_pos, 2)
                i -= 1
        except ValueError:
            pass

        try:
            i = 0
            while True:
                start_pos = self.rect.topleft + i * self.line_spacing + self.line_offset
                end_pos = self.rect.topright + i * self.line_spacing
                start_pos, end_pos = self.rect.clipline(start_pos, end_pos)
                pygame.draw.line(rect_surface, self.color, start_pos, end_pos, 2)
                i += 1
        except ValueError:
            pass
        text = self.font.render("Next stage", True, 'red')
        dest = pygame.Vector2(rect_surface.get_rect().center) - pygame.Vector2(text.get_rect().size) // 2
        rect_surface.blit(text, dest)
        return rect_surface.convert_alpha()

    def draw(self, surface: pygame.Surface, position: pygame.Vector2):
        surface.blit(self.rect_surface, position)
