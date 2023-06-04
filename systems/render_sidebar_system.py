import pygame

from systems.system import *

class RenderSidebarSystem(System):
    def on_update(self):
        health_bars = []
        surface = pygame.display.get_surface()
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
            x = surface.get_width() - health_bar.get_width() - 10
            y = id * (health_bar.get_height() + 20) + 20
            surface.blit(health_bar, (x, y))

