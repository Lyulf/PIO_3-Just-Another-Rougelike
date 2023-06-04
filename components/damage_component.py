from components.component import *

class DamageComponent(Component):
    def __init__(self, damage, piercing):
        self.damage = damage
        self.piercing = piercing
