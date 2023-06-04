from entities.entity import Entity
from components.component import Component


class ComponentManager(object):
    def __init__(self):
        self.components = {}

    def add_component(self, entity: Entity, component: Component):
        try:
            self.components[entity.id][type(component)] = component
        except KeyError:
            self.components[entity.id] = {type(component): component}

    def get_components(self, entity: Entity, *component_types: type):
        components = self.components.get(entity.id, {})
        if not component_types:
            return components
        else:
            components = {component_type: component for component_type, component in components.items() if component_type in component_types}
            return components

    def get_component(self, entity: Entity, component_type: type):
        try:
            return self.components[entity.id][component_type]
        except KeyError:
            return None

    def remove_components(self, entity):
        try:
            del self.components[entity.id]
        except KeyError:
            pass

