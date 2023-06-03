from systems.system import *

class HealthSystem(System):
    def on_update(self):
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, HealthComponent, ImageSpriteComponent)
            try:
                health = components[HealthComponent]
                image_sprite = components[ImageSpriteComponent]
            except (TypeError, KeyError):
                continue

            if health.current_health <= 0:
                try:
                    image_sprite.current_sprite = image_sprite.sprite_sheets['death']
                    if image_sprite.current_sprite.is_finished:
                        entity.is_alive = False
                except KeyError:
                    entity.is_alive = False
                    continue
            elif health.was_hurt:
                try:
                    image_sprite.current_sprite = image_sprite.sprite_sheets['hurt']
                except KeyError:
                    continue
                finally:
                    health.was_hurt = False

