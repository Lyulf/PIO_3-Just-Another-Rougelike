from components.component import *
from entities.entity_type import *

class HealthComponent(Component):
    def __init__(self, max_health, entity_type: EntityType, grace_period=0, current_health=None):
        self.max_health = max_health
        self.entity_type = entity_type
        self.current_health = current_health if current_health is not None else max_health
        self.was_hurt = False
        self.last_damage_time_tick = 0
        self.grace_period = grace_period * 1000
