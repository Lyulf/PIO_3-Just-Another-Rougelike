from components.component import *
from enum import Enum

class WeaponType(Enum):
    PISTOL = 1
    SHOTGUN = 2
    RIFLE = 3

class WeaponComponent(Component):
    def __init__(self, projectile_count, spread_angle, fire_delay, weapon_type):
        self.projectile_count = projectile_count
        self.spread_angle = spread_angle
        self.fire_delay = fire_delay
        self.last_fire_time = 0
        self.weapon_type = weapon_type
