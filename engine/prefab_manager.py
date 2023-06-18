from components import *
from engine.component_manager import ComponentManager
from engine.entity_manager import EntityManager

class PrefabManager(object):
    def __init__(self, entity_manager: EntityManager, component_manager: ComponentManager):
        self.entity_manager = entity_manager
        self.component_manager = component_manager
        self.prefabs = {}

    def get_prefab(self, name):
        return self.prefabs[name]

    def set_prefab(self, name, prefab):
        prefab.late_init(self.entity_manager, self.component_manager)
        self.prefabs[name] = prefab

    def spawn(self, prefab_name, position):
        prefab = self.get_prefab(prefab_name)
        entity = self.entity_manager.create_entity()
        components = prefab.create(pygame.Vector2(position))
        entity_position = components[TransformComponent].position
        self.component_manager.add_components(entity, *components.values())
        for child_prefab in prefab.prefabs:
            self.spawn(child_prefab, entity_position)
        return entity