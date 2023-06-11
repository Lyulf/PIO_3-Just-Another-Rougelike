import pygame

from enum import Enum
from systems.collision_system import *
from systems.damage_system import *
from systems.system import *
from systems.user_input_system import *


class GameStates(Enum):
    GO_NEXT_AREA = 0
    CHANGING_STAGES = 1
    NEW_STAGE_INTRO = 2
    FIGHTING = 3


class GameStateSystem(System):
    def __init__(self, window_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_size = window_size

    def on_create(self):
        self.state = GameStates.GO_NEXT_AREA
        self.go_next_area = None
        self.start_animation = 0
        self.end_animation = 0
        self.camera_start_pos = pygame.Vector2()
        self.camera_end_pos = pygame.Vector2()
        for entity in self.entity_manager.get_entities():
            if self.component_manager.get_component(entity, CameraComponent):
                self.camera = entity
                break
        else:
            raise RuntimeError("No camera")
        self.on_update()

    def on_update(self):
        disabled_systems = []
        if self.state == GameStates.GO_NEXT_AREA:
            if not self.go_next_area:
                self.go_next_area = self.prefab_manager.spawn('go_next_stage_area', pygame.Vector2(360, 90))
        if self.state == GameStates.CHANGING_STAGES:
            if self.go_next_area:
                self.go_next_area.is_alive = False
                self.go_next_area = None
            disabled_systems = [UserInputSystem, DamageSystem]
            ticks = pygame.time.get_ticks() - self.start_animation
            animation_time = self.end_animation - self.start_animation
            camera_transform = self.component_manager.get_component(self.camera, TransformComponent)
            if ticks <= animation_time:
                camera_transform.position = self.camera_start_pos.lerp(self.camera_end_pos, ticks / animation_time)
            else:
                self.state = GameStates.NEW_STAGE_INTRO
                camera_transform.position = pygame.Vector2()
                for entity in self.entity_manager.get_entities():
                    components = self.component_manager.get_components(entity, TransformComponent, RigidbodyComponent, PlayerComponent, EnemyAiComponent, ItemComponent)
                    if EnemyAiComponent in components.keys():
                        entity.is_alive = False
                        continue
                    if ItemComponent in components.keys():
                        entity.is_alive = False
                        continue
                    try:
                        player_component = components[PlayerComponent]
                        transform = components[TransformComponent]
                        rigidbody = components[RigidbodyComponent]
                    except (TypeError, KeyError):
                        continue
                    transform.position = pygame.Vector2(6.5 * self.window_size[0] / 16, self.window_size[1] + 100)
                    rigidbody.direction = pygame.Vector2(0, -1)
        if self.state == GameStates.NEW_STAGE_INTRO:
            disabled_systems = [UserInputSystem, CollisionSystem]
            for entity in self.entity_manager.get_entities():
                components = self.component_manager.get_components(entity, TransformComponent, RigidbodyComponent, PlayerComponent)
                try:
                    player_component = components[PlayerComponent]
                    transform = components[TransformComponent]
                    rigidbody = components[RigidbodyComponent]
                except (TypeError, KeyError):
                    continue
                if transform.position.y <= 6 * self.window_size[1] / 8:
                    rigidbody.direction = pygame.Vector2(0, 0)
                    self.state = GameStates.FIGHTING
        if self.state == GameStates.FIGHTING:
            pass

        for system in self.systems_manager.get_systems():
            system.enabled = type(system) not in disabled_systems

    def go_to_next_stage(self):
        ticks = pygame.time.get_ticks()
        self.state = GameStates.CHANGING_STAGES
        self.start_animation = ticks
        self.end_animation = ticks + 1000 # ms
        camera_transform = self.component_manager.get_component(self.camera, TransformComponent)
        self.camera_start_pos = camera_transform.position
        self.camera_end_pos = camera_transform.position + pygame.Vector2(0, -self.window_size[1])
        camera_transform.position.y -= self.window_size[1] // 20
