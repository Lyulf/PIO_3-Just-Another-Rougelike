from components.component import *
from entities.entity_type import *

class DamageComponent(Component):
    def __init__(self, damage, piercing, ignore_entity_types: list[EntityType] = None):
        self.damage = damage
        self.piercing = piercing
        self.ignore_entity_types = ignore_entity_types if ignore_entity_types is not None else []
