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

    def __init__(self):
        self.entity_manager = EntityManager()
        self.component_manager = ComponentManager()
        self.system_manager = SystemManager()
        self.prefab_manager = PrefabManager(self.entity_manager, self.component_manager)

        self.add_system(0, UserInputSystem)
        self.add_system(1, EnemyAiSystem)
        self.add_system(2, MovementSystem)
        self.add_system(3, DamageSystem)
        self.add_system(4, CollisionSystem)
        self.add_system(5, HealthSystem)
        self.add_system(6, RenderSystem)
        self.add_system(6, RenderSidebarSystem)

        for player_id in range(4):
            self.prefab_manager.set_prefab(f'player{player_id + 1}', PlayerPrefab(player_id))

        self.prefab_manager.set_prefab('demon', DemonPrefab())
        self.prefab_manager.set_prefab('basic_projectile', BasicProjectilePrefab('green'))

    def add_system(self, priority: int, system_type: type, *args, **kwargs):
        system = system_type(
            self.entity_manager,
            self.component_manager,
            self.prefab_manager,
            *args,
            **kwargs)
        self.system_manager.add_system(priority, system)

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
        for dead_entity in self.entity_manager.garbage_collect_entities():
            self.component_manager.remove_components(dead_entity)

        for system in self.system_manager.get_systems():
            system.on_update()

