import math
import pickle
import pygame
import random
from engine.entity_manager import EntityManager
from engine.component_manager import ComponentManager
from engine.system_manager import SystemManager
from engine.prefab_manager import PrefabManager

from entities import *
from systems import *
from prefabs import *

from utils.delta_time import *
from utils.border import get_border

class GameEngine(object):
    """Class handling game physics."""

    def __init__(self, window_size):
        self.window_size = window_size
        self.entity_manager = EntityManager()
        self.component_manager = ComponentManager()
        self.system_manager = SystemManager()
        self.prefab_manager = PrefabManager(self.entity_manager, self.component_manager)
        self.current_stage = None
        self.next_stage = None

        self.add_system(0, UserInputSystem)
        self.add_system(1, EnemyAiSystem)
        self.add_system(2, MovementSystem)
        self.add_system(3, DamageSystem)
        self.add_system(4, CollisionSystem)
        self.add_system(5, HealthSystem)
        self.game_state_system = self.add_system(6, GameStateSystem, self.window_size)
        self.add_system(7, RenderSystem)
        self.add_system(7, RenderSidebarSystem, self.window_size)

        for player_id in range(4):
            self.prefab_manager.set_prefab(f'player{player_id + 1}', PlayerPrefab(player_id))

        self.prefab_manager.set_prefab('demon', DemonPrefab())
        self.prefab_manager.set_prefab('basic_projectile', BasicProjectilePrefab('green'))
        self.prefab_manager.set_prefab('item', ItemPrefab())
        self.prefab_manager.set_prefab('go_next_stage_area', GoNextStageAreaPrefab('orange4', self.game_state_system))

        self.__add_camera()
        self.__add_stage()
        self.__add_next_stage()

    def add_system(self, priority: int, system_type: type, *args, **kwargs):
        system = system_type(
            *args,
            self.entity_manager,
            self.component_manager,
            self.system_manager,
            self.prefab_manager,
            **kwargs)
        self.system_manager.add_system(priority, system)
        return system

    def __add_camera(self):
        camera = self.entity_manager.create_entity()
        self.component_manager.add_component(camera, TransformComponent())
        self.component_manager.add_component(camera, RigidbodyComponent(0, CollisionType.KINETIC, pygame.Vector2(0, -1)))
        self.component_manager.add_component(camera, CameraComponent())

    def __add_stage(self):
        if self.next_stage:
            self.current_stage.is_alive = False
            self.current_stage = self.next_stage
            self.next_stage = None
            return
        self.current_stage = self.entity_manager.create_entity()
        transform = TransformComponent()
        self.component_manager.add_component(self.current_stage, transform)
        stage_component = StageComponent(1)
        self.component_manager.add_component(self.current_stage, stage_component)
        rect = pygame.Rect((0, 0), self.window_size)
        anchor = rect.topleft
        sprite = pygame.transform.scale(get_sprite('resources/Map/plansza.png', True), self.window_size)
        sprites = {
            'idle': ui.spritesheet.SpriteSheet(
                sprite, sprite.get_width(), sprite.get_height(), 0, 1, False)
            }
        image_sprite = ImageSpriteComponent(rect, anchor, sprites, 'idle')
        self.component_manager.add_component(self.current_stage, image_sprite)

    def __add_next_stage(self):
        if self.next_stage:
            self.next_stage.is_alive = False
        self.next_stage = self.entity_manager.create_entity()
        transform = TransformComponent(position=pygame.Vector2(0, -self.window_size[1] - 10))
        self.component_manager.add_component(self.next_stage, transform)
        current_stage_component = self.component_manager.get_component(self.current_stage, StageComponent)
        stage_component = StageComponent(current_stage_component.stage_number)
        self.component_manager.add_component(self.next_stage, stage_component)
        rect = pygame.Rect((0, 0), self.window_size)
        anchor = rect.topleft
        sprite = pygame.transform.scale(get_sprite('resources/Map/plansza.png', True), self.window_size)
        sprites = {
            'idle': ui.spritesheet.SpriteSheet(
                sprite, sprite.get_width(), sprite.get_height(), 0, 1, False)
            }
        image_sprite = ImageSpriteComponent(rect, anchor, sprites, 'idle')
        self.component_manager.add_component(self.next_stage, image_sprite)

    def create(self):
        for system in self.system_manager.get_systems():
            system.on_create()

    def destroy(self):
        for system in self.system_manager.get_systems():
            system.on_destroy()

    def spawn_players(self, number_of_players):
        """Spawns players evenly distributed around the whole map."""
        players = [None] * number_of_players
        rows = math.floor(math.sqrt(number_of_players))
        columns = math.ceil(number_of_players / rows)
        last_column = math.floor(number_of_players / rows)
        columns_in_row = [columns if row != rows - 1 else last_column for row in range(rows)]
        border = get_border()
        spacing_y = border.y + border.height // (rows - 1 + 2)
        k = 0
        for i in range(rows):
            spacing_x = border.x + border.width // (columns - 1 + 2)
            columns = columns_in_row[i]
            for j in range(columns):
                y = (i % rows + 1) * spacing_y
                x = (j % columns + 1) * spacing_x
                player = self.__create_player((x, y), k)
                players[k - number_of_players] = player
                k += 1
        return players

    def spawn_opponents(self, number_of_opponents):
        """Spawns opponents evenly distributed around the whole map."""
        opponents = [None] * number_of_opponents
        rows = math.floor(math.sqrt(number_of_opponents))
        columns = math.ceil(number_of_opponents / rows)
        last_column = math.floor(number_of_opponents / rows)
        columns_in_row = [columns if row != rows - 1 else last_column for row in range(rows)]
        border = get_border()
        spacing_y = border.y + border.height // (rows - 1 + 2)
        k = 0
        for i in range(rows):
            spacing_x = border.x + border.width // (columns - 1 + 2)
            columns = columns_in_row[i]
            for j in range(columns):
                y = (i % rows + 1) * spacing_y
                x = (j % columns + 1) * spacing_x
                opponent = self.__create_opponent((x, y))
                opponents[k - number_of_opponents] = opponent
                k += 1
        return opponents

    def __create_player(self, position, id):
        return self.prefab_manager.spawn(f'player{id + 1}', position)

    def __create_opponent(self, position):
        return self.prefab_manager.spawn('demon', position)


    def update(self):
        """Update systems"""
        ticks = pygame.time.get_ticks()
        for dead_entity in self.entity_manager.garbage_collect_entities():
            self.component_manager.remove_components(dead_entity)
        if current_dt() >= 50:
            for system in self.system_manager.get_systems():
                if system.enabled:
                    system.on_fixed_update()
            update_dt(0)
        for system in self.system_manager.get_systems():
            if system.enabled:
                system.on_update()

