import random
from enum import Enum
from systems import GameStates, GameStateSystem
from systems.system import *

class SpawnDirection(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2

class EnemySpawnSystem(System):

    def on_create(self):
        self.game_state_system = self.systems_manager.get_system(GameStateSystem)
        self.max_enemies_on_stage = 5
        self.max_enemies_at_once = 3
        self.spawned_enemies = 0
        self.on_update()


    def on_fixed_update(self):
        if self.game_state_system.state == GameStates.CHANGING_STAGES:
            return
        if self.game_state_system.state == GameStates.NEW_STAGE_INTRO:
            self.spawned_enemies = 0
        enemies_alive = 0
        for entity in self.entity_manager.get_entities():
            if self.component_manager.get_component(entity, EnemyAiComponent):
                enemies_alive += 1
        if self.spawned_enemies == self.max_enemies_on_stage and enemies_alive == 0:
            self.game_state_system.state = GameStates.GO_NEXT_AREA
        elif self.game_state_system.state == GameStates.FIGHTING:
            if enemies_alive != self.max_enemies_at_once and self.spawned_enemies < self.max_enemies_on_stage:
                spawn_direction = random.choice(list(SpawnDirection))
                if spawn_direction == SpawnDirection.LEFT:
                    self.prefab_manager.spawn('demon', pygame.Vector2(-1, 380))
                elif spawn_direction == SpawnDirection.RIGHT:
                    self.prefab_manager.spawn('demon', pygame.Vector2(961, 380))
                elif spawn_direction == SpawnDirection.UP:
                    self.prefab_manager.spawn('demon', pygame.Vector2(520, -1))
                self.spawned_enemies += 1




