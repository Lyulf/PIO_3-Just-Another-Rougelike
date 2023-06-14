from systems import GameStates, GameStateSystem
from systems.system import *


class EnemySpawnSystem(System):

    def __init__(self, entity_manager: EntityManager, component_manager: ComponentManager,
                 systems_manager: SystemManager, prefab_manager: PrefabManager):
        super().__init__(entity_manager, component_manager, systems_manager, prefab_manager)
        self.game_state_system = self.systems_manager.get_system(GameStateSystem)
        self.max_enemies_on_stage = 5
        self.max_enemies_at_once = 3
        self.spawned_enemies = 0

    def on_create(self):
        self.on_update()

    def on_update(self):
        pass

    def on_fixed_update(self):
        if self.game_state_system.state == GameStates.CHANGING_STAGES:
            return
        if self.game_state_system.state == GameStates.NEW_STAGE_INTRO:
            self.spawned_enemies = 0
        enemiesAlive = 0
        for entity in self.entity_manager.get_entities():
            if self.component_manager.get_component(entity, EnemyAiComponent):
                enemiesAlive += 1
        if self.max_enemies_at_once > self.max_enemies_on_stage:
            self.max_enemies_at_once = self.max_enemies_on_stage
        if self.spawned_enemies == self.max_enemies_on_stage and enemiesAlive == 0:
            self.game_state_system.state = GameStates.GO_NEXT_AREA
        if self.game_state_system.state == GameStates.FIGHTING and enemiesAlive != self.max_enemies_at_once \
                and self.spawned_enemies < self.max_enemies_on_stage:
            if enemiesAlive % 2 == 0:
                self.prefab_manager.spawn('demon', pygame.Vector2(-1, 380))
                self.spawned_enemies += 1
            else:
                self.prefab_manager.spawn('demon', pygame.Vector2(961, 380))
                self.spawned_enemies += 1


