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
        projectile = self.entity_manager.create_entity()
        entity_components = self.component_manager.get_components(entity, TransformComponent, RigidbodyComponent, RectHitboxComponent)
        try:
            entity_transform = entity_components[TransformComponent]
            entity_rigidbody = entity_components[RigidbodyComponent]
        except (TypeError, KeyError):
            return
        projectile_transform = TransformComponent(
            entity_transform.position.copy(),
            entity_transform.rotation,
            entity_transform.scale.copy(),
        )
        self.component_manager.add_component(projectile, projectile_transform)
        projectile_direction = (mouse_vector - entity_transform.position).normalize()
        projectile_rigidbody = RigidbodyComponent(
            3,
            CollisionType.KINETIC,
            projectile_direction,
        )
        self.component_manager.add_component(projectile, projectile_rigidbody)
        rect = pygame.Rect(0, 0, 20, 20)
        anchor = pygame.Vector2(rect.center)
        ignore_entity_types = [EntityType.PROJECTILE]
        try:
            entity_rect_hitbox = entity_components[RectHitboxComponent]
            ignore_entity_types.append(entity_rect_hitbox.entity_type)
        except KeyError:
            pass
        projectile_rect_hitbox = RectHitboxComponent(
            rect, anchor, EntityType.PROJECTILE, ignore_entity_types
        )
        self.component_manager.add_component(projectile, projectile_rect_hitbox)
        projectile_rect_sprite = RectSpriteComponent(rect, anchor, 'green')
        self.component_manager.add_component(projectile, projectile_rect_sprite)
        damage = DamageComponent(1, False, ignore_entity_types)
        self.component_manager.add_component(projectile, damage)
