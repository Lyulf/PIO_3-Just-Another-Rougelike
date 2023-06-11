import pygame

from components.component import *
from utils.resources import get_sprite

class StageComponent(Component):
    def __init__(self, stage_number):
        self.stage_number = stage_number