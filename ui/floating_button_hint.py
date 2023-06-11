import pygame

from utils.resources import get_sprite

class FloatingButtonHint(object):
    def __init__(self, button: str, font: pygame.font.Font = None):
        self.text_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        background = get_sprite('resources/icons/keyboard-key-empty.png', True)
        background = pygame.transform.scale(background, self.text_surface.get_rect().size)
        self.text_surface.blit(background, (0, 0))
        font = font if font is not None else pygame.font.Font('resources/mainMenu/font.ttf', 20)
        text = font.render(button, True, 'white')
        dest = pygame.Vector2(background.get_rect().center) - pygame.Vector2(text.get_rect().size) // 2
        self.text_surface.blit(text, dest + pygame.Vector2(2, 0))
    
    def draw(self, surface: pygame.Surface, position: pygame.Vector2):
        surface.blit(self.text_surface, position - self.text_surface.get_rect().center)
        