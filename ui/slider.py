import pygame

class Slider:
    def __init__(self, width, height, x_pos, y_pos, color, active_color, value):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.active_color = active_color
        self.value = value
        self.active = False
        self.stroke_color = "RED"
        self.stroke_width = 5
        self.rect = pygame.Rect(self.x_pos, self.y_pos, int(self.value * self.width), self.height)

    def update_slider_value(self, mouse_pos):
        self.value = (mouse_pos - self.x_pos) / self.width
        self.value = max(0, min(1, self.value))

    def draw(self, screen):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, int(self.value * self.width), self.height)
        stroke_rect = pygame.Rect(self.x_pos-self.stroke_width, self.y_pos-self.stroke_width,
                                  int(self.width + (2 * self.stroke_width)), (2 * self.stroke_width) + self.height)
        slider_color = self.active_color if self.active else self.color
        pygame.draw.rect(screen, self.stroke_color, stroke_rect)
        pygame.draw.rect(screen, slider_color, self.rect)
