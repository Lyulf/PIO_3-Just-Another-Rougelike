import pygame

from components import *
from systems.system import *


class UserInputSystem(System):
    def on_create(self):
        self.keys_down = []
        self.held_keys = {}
        self.last_spawn_time = 0

    def on_update(self):
        delay_time = 250  # Delay time in milliseconds (0.5 seconds)
        camera = None
        for entity in self.entity_manager.get_entities():
            if self.component_manager.get_component(entity, CameraComponent):
                camera = entity
                break
        try:
            camera_position = self.component_manager.get_component(camera, TransformComponent).position
        except AttributeError:
            camera_position = pygame.Vector2()

        interactables = []
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, TransformComponent, InteractionComponent)
            try:
                transform = components[TransformComponent]
                interaction_component = next(c for c in components.values() if isinstance(c, InteractionComponent))
            except (KeyError, TypeError, StopIteration):
                continue
            interaction_rect = interaction_component.rect.move(transform.position - interaction_component.anchor)
            interactables.append((entity, interaction_rect, interaction_component.interaction))

        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, TransformComponent, ControlsComponent, RigidbodyComponent)
            try:
                transform = components[TransformComponent]
                controls = components[ControlsComponent]
                rigidbody = components[RigidbodyComponent]
            except (TypeError, KeyError):
                continue
            try:
                mouse_pos = pygame.mouse.get_pos()
                mouse_vector = pygame.Vector2(*mouse_pos) + camera_position
                pygame.event.get()
                if pygame.mouse.get_pressed()[0]:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_spawn_time >= delay_time:
                        self.last_spawn_time = current_time
                        self.__spawn_projectile(entity, mouse_vector)
            except IndexError:
                pass

            min_distance = math.inf
            current_interaction = None
            current_interactable_entity = None

            for interactable_entity, rect, interaction in interactables:
                if rect.collidepoint(transform.position):
                    distance = pygame.Vector2(rect.center) - transform.position
                    distance_squared = distance.magnitude_squared()
                    if distance_squared < min_distance:
                        min_distance = distance_squared
                        current_interactable_entity = interactable_entity
                        current_interaction = interaction

            for hint_entity in self.entity_manager.get_entities():
                try:
                    hint = self.component_manager.get_component(hint_entity, InteractionHint)
                    if hint.owner.id == entity.id:
                        if current_interaction is not None:
                            hint.visible = True
                        else:
                            hint.visible = False
                except AttributeError:
                    continue

            try:
                keys_down = self.keys_down.copy()
                while True:
                    key = keys_down.pop(0)
                    if key == controls.custom_keys[Controls.USE] and current_interaction:
                        current_interaction(entity, current_interactable_entity)
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