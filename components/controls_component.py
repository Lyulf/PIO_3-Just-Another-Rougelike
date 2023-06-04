from components.component import *
from enum import Enum

class Controls(Enum):
    UP = 0,
    LEFT = 1,
    DOWN = 2,
    RIGHT = 3,
    SHOOT = 4,
    USE = 5,


class ControlsComponent(Component):
    def __init__(self, custom_keys: dict):
        self.custom_keys = custom_keys