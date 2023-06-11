import pygame

from systems.system import *

class RenderSidebarSystem(System):
    def __init__(self, window_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sidebar_rect = pygame.Rect(13 * window_size[0] // 16, 0, 3 * window_size[0] // 16, window_size[1])

    def on_update(self):
        health_bars = []
        surface = pygame.display.get_surface()
        pygame.draw.rect(surface, pygame.Color(43, 42, 41), self.sidebar_rect)
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, PlayerComponent, PlayerSidebarHealthBarComponent, HealthComponent)
            try:
                player_component = components[PlayerComponent]
                health_bar = components[PlayerSidebarHealthBarComponent]
                health = components[HealthComponent]
            except (TypeError, KeyError):
                continue
            try:
                sprite = health_bar.sprites[max(health.current_health, 0)]
                width = 200
                aspect_ratio = sprite.get_width() // sprite.get_height()
                height = width // aspect_ratio
                sprite = pygame.transform.scale(sprite, (width, height))
                if player_component.is_current_player:
                    health_bars.append((0, sprite))
                else:
                    health_bars.append((player_component.player_id + 1, sprite))
            except IndexError:
                continue

        for id, (_, health_bar) in enumerate(sorted(health_bars, key=lambda x: x[0])):
            x = self.sidebar_rect.centerx - health_bar.get_rect().centerx
            y = id * (health_bar.get_height() + 20) + 20
            surface.blit(health_bar, (x, y))

