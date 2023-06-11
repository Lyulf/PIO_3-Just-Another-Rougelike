from components import *
from engine.component_manager import ComponentManager
from engine.entity_manager import EntityManager
from engine.prefab_manager import PrefabManager
from utils.delta_time import *

class System(object):
    def __init__(self, entity_manager: EntityManager, component_manager: ComponentManager, prefab_manager: PrefabManager):
        self.entity_manager = entity_manager
        self.component_manager = component_manager
        self.prefab_manager = prefab_manager

    def on_create(self):
        pass

    def on_update(self):
        pass

    def on_destroy(self):
        pass