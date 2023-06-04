import math
import pickle
import pygame
import random
import ui.spritesheet

from engine.entity_manager import EntityManager
from engine.component_manager import ComponentManager
from engine.system_manager import SystemManager

from entities import *
from systems import *

from utils.delta_time import *
from utils.border import get_border

class GameEngine(object):
    """Class handling game physics."""
    CHARACTER_WIDTH = 50
    CHARACTER_HEIGHT = 50
    OPPONENT_WIDTH = 50
    OPPONENT_HEIGHT = 50
    OPPONENT_SPEED = 0.2
    PLAYER_SPEED = 1

    def __init__(self):
        self.entity_manager = EntityManager()
        self.component_manager = ComponentManager()
        self.system_manager = SystemManager()
        self.sprites = None

        self.add_system(0, UserInputSystem)
        self.add_system(1, EnemyAiSystem)
        self.add_system(2, MovementSystem)
        self.add_system(3, CollisionSystem)
        self.add_system(4, HealthSystem)
        self.add_system(5, RenderSystem)
        self.add_system(5, RenderSidebarSystem)

    def add_system(self, priority: int, system_type: type, *additional_args):
        self.system_manager.add_system(priority, system_type(self.entity_manager, self.component_manager, *additional_args))

    def load_images(self):
        self.sprites = {
            'demon': {
                'idle_sprite': pygame.image.load("resources/enemies/demon/idle.png"),
                'walk_sprite': pygame.image.load("resources/enemies/demon/walk.png"),
                'hurt_sprite': pygame.image.load("resources/enemies/demon/hurt.png"),
                'attack_sprite': pygame.image.load("resources/enemies/demon/attack.png"),
                'death_sprite': pygame.image.load("resources/enemies/demon/death.png"),
            },
            'player': {
                'idle_sprite': pygame.image.load("resources/playerModel/idle.png"),
                'left_sprite': pygame.image.load("resources/playerModel/left.png"),
                'right_sprite': pygame.image.load("resources/playerModel/right.png"),
                'down_sprite': pygame.image.load("resources/playerModel/down.png"),
                'up_sprite': pygame.image.load("resources/playerModel/up.png"),
            },
            'health_bar': [
                pygame.image.load(f"resources/HP_Bar/{id}.png") for id in range(11)
            ]
        }

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
                player = self.__create_player(x, y, False)
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
                opponent = self.__create_opponent(x, y)
                opponents[k - number_of_opponents] = opponent
                k += 1
        return opponents

    def __create_player(self, x, y, is_current_player, id=None):
        player = self.entity_manager.create_entity()
        transform = TransformComponent(pygame.Vector2(x, y), 0, pygame.Vector2(1, 1))
        self.component_manager.add_component(player, transform)
        rigidbody = RigidbodyComponent(self.PLAYER_SPEED)
        self.component_manager.add_component(player, rigidbody)
        player_rect = pygame.Rect(0, 0, self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT)
        anchor = pygame.Vector2(player_rect.center)
        rect_hitbox = RectHitboxComponent(player_rect, anchor, EntityTypes.PLAYER, [EntityTypes.PLAYER])
        self.component_manager.add_component(player, rect_hitbox)
        old_color = pygame.Color(246, 187, 148)
        new_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        sprites = self.sprites['player']
        sprite_sheets = {
            'idle' : ui.spritesheet.SpriteSheet(sprites['idle_sprite'], 16, 16, 500, 6, True, old_color, new_color),
            'left' : ui.spritesheet.SpriteSheet(sprites['left_sprite'], 16, 16, 250, 6, True, old_color, new_color),
            'right' : ui.spritesheet.SpriteSheet(sprites['right_sprite'], 16, 16, 250, 6, True, old_color, new_color),
            'down' : ui.spritesheet.SpriteSheet(sprites['down_sprite'], 16, 16, 250, 6, True, old_color, new_color),
            'up' : ui.spritesheet.SpriteSheet(sprites['up_sprite'], 16, 16, 250, 6, True, old_color, new_color),
        }
        offset = pygame.Vector2(0, -50)
        sprite = ImageSpriteComponent(player_rect.copy(), anchor.copy(), sprite_sheets, 'idle', offset)
        self.component_manager.add_component(player, sprite)
        health = HealthComponent(10)
        self.component_manager.add_component(player, health)
        player_component = PlayerComponent(is_current_player, id)
        self.component_manager.add_component(player, player_component)
        sidebar_health_bar = PlayerSidebarHealthBarComponent(self.sprites['health_bar'])
        self.component_manager.add_component(player, sidebar_health_bar)
        return player

    def __create_opponent(self, x, y):
        opponent = self.entity_manager.create_entity()
        transform = TransformComponent(pygame.Vector2(x, y), 0, pygame.Vector2(1, 1))
        self.component_manager.add_component(opponent, transform)
        rigidbody = RigidbodyComponent(self.OPPONENT_SPEED)
        self.component_manager.add_component(opponent, rigidbody)
        opponent_rect = pygame.Rect(0, 0, self.OPPONENT_WIDTH, self.OPPONENT_HEIGHT)
        anchor = pygame.Vector2(opponent_rect.center)
        rect_hitbox = RectHitboxComponent(opponent_rect, anchor, EntityTypes.ENEMY, [])
        self.component_manager.add_component(opponent, rect_hitbox)
        sprites = self.sprites['demon']
        sprite_sheets = {
            'idle' : ui.spritesheet.SpriteSheet(sprites['idle_sprite'], 256, 256, 350, 1, False),
            'walk' : ui.spritesheet.SpriteSheet(sprites['walk_sprite'], 256, 256, 100, 1, False),
            'hurt' : ui.spritesheet.SpriteSheet(sprites['hurt_sprite'], 256, 256, 100, 1, False),
            'attack' : ui.spritesheet.SpriteSheet(sprites['attack_sprite'], 256, 256, 100, 1, False),
            'death' : ui.spritesheet.SpriteSheet(sprites['death_sprite'], 256, 256, 100, 1, False),
        }
        offset = pygame.Vector2(34, -50)
        sprite = ImageSpriteComponent(opponent_rect.copy(), anchor.copy(), sprite_sheets, 'idle', offset)
        self.component_manager.add_component(opponent, sprite)
        health = HealthComponent(10)
        self.component_manager.add_component(opponent, health)
        enemy_ai = EnemyAiComponent(AiType.BASIC)
        self.component_manager.add_component(opponent, enemy_ai)
        return opponent

    def update(self):
        """Update systems"""
        for dead_entity in self.entity_manager.garbage_collect_entities():
            self.component_manager.remove_components(dead_entity)

        for system in self.system_manager.get_systems():
            system.on_update()

