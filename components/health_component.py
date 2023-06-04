from components.component import *

class HealthComponent(Component):
    def __init__(self, max_health, current_health=None):
        self.max_health = max_health
        self.current_health = current_health if current_health is not None else max_health
        self.was_hurt = False
