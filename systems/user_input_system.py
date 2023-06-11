from components import *
from systems.system import *

import pygame

class UserInputSystem(System):
    def on_create(self):
        self.keys_down = []
        self.held_keys = {}
        self.last_spawn_time = 0
    def on_update(self):
        delay_time = 250  # Delay time in milliseconds (0.5 seconds)
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, ControlsComponent, RigidbodyComponent)
            try:
                controls = components[ControlsComponent]
                rigidbody = components[RigidbodyComponent]
            except (TypeError, KeyError):
                continue
            try:
                mouse_pos = pygame.mouse.get_pos()
                mouse_vector = pygame.Vector2(*mouse_pos)
                pygame.event.get()
                if pygame.mouse.get_pressed()[0]:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_spawn_time >= delay_time:
                        self.last_spawn_time = current_time
                        self.__spawn_projectile(entity, mouse_vector)
            except IndexError:
                pass
            direction = pygame.Vector2()
            if self.held_keys[controls.custom_keys[Controls.UP]]:
                direction.y -= 1
            if self.held_keys[controls.custom_keys[Controls.DOWN]]:
                direction.y += 1
            if self.held_keys[controls.custom_keys[Controls.LEFT]]:
                direction.x -= 1
            if self.held_keys[controls.custom_keys[Controls.RIGHT]]:
                direction.x += 1
            try:
                rigidbody.direction = direction.normalize()
            except ValueError:
                rigidbody.direction = pygame.Vector2()
        self.keys_down = []

    def __spawn_projectile(self, entity, mouse_vector):
        entity_components = self.component_manager.get_components(entity, TransformComponent, RectHitboxComponent)
        try:
            entity_transform = entity_components[TransformComponent]
        except (TypeError, KeyError):
            return

        projectile = self.prefab_manager.spawn('basic_projectile', entity_transform.position)
        projectile_components = self.component_manager.get_components(projectile, RigidbodyComponent, DamageComponent)
        projectile_rigidbody = projectile_components[RigidbodyComponent]
        try:
            projectile_rigidbody.direction = mouse_vector - entity_transform.position
            projectile_rigidbody.direction.normalize_ip()
        except ValueError:
            projectile_rigidbody.direction = pygame.Vector2()

        projectile_damage = projectile_components[DamageComponent]
        try:
            entity_rect_hitbox = entity_components[RectHitboxComponent]
        except KeyError:
            return
        projectile_damage.ignore_entity_types.append(entity_rect_hitbox.entity_type)