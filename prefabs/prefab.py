from components import *

from engine.entity_manager import EntityManager
from engine.component_manager import ComponentManager


class Prefab(object):
    def __init__(self, prefabs=None):
        self.prefabs = prefabs if prefabs is not None else []

    def late_init(self, entity_manager: EntityManager, component_manager: ComponentManager):
        self.entity_manager = entity_manager
        self.component_manager = component_manager

    def create(self, position: pygame.Vector2):
        return {TransformComponent: TransformComponent(pygame.Vector2(position), 0, pygame.Vector2(1, 1))}

    def add_prefab(self, prefab):
        self.prefabs.append(prefab)

    def _add_component(self, components, component):
        if component in components:
            raise KeyError
        components[type(component)] = component