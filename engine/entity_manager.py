import uuid

from entities.entity import Entity

class EntityManager(object):
    def __init__(self):
        self.entities = {}

    def create_entity(self):
        id = uuid.uuid4()
        entity = Entity(id)
        self.entities[id] = entity
        return entity

    def get_entities(self):
        return list(entity for entity in self.entities.values() if entity.is_alive)

    def get_entity(self, id: uuid.UUID):
        try:
            entity = self.entities[id]
            if entity.is_alive:
                return entity
        except KeyError:
            pass
        return None

    def garbage_collect_entities(self):
        dead_entities = [entity for entity in self.entities.values() if not entity.is_alive]
        for entity in dead_entities:
            self.remove_entity(entity.id)
            yield entity

    def remove_entity(self, id: uuid.UUID):
        try:
            del self.entities[id]
        except KeyError:
            pass
