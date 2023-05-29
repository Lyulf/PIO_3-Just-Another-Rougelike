import pygame
import math

from entities import *

class GameEngine(object):
    """Class handling game physics."""
    CHARACTER_WIDTH = 50
    CHARACTER_HEIGHT = 100
    PLAYER_SPEED = 1

    def __init__(self):
        self.entities = []
        self.background_rect = None

    def set_background_rect(self, rect):
        """Sets background rectangle.

        It should be windows rectangle or map rectangle."""
        self.background_rect = rect

    def spawn_players(self, number_of_players):
        """Spawns players evenly distributed around the whole map."""
        self.entities += [None] * number_of_players
        rows = math.floor(math.sqrt(number_of_players))
        columns = math.ceil(number_of_players / rows)
        last_column = math.floor(number_of_players / rows)
        columns_in_row = [columns if row != rows - 1 else last_column for row in range(rows)]
        spacing_y = self.background_rect.height // (rows - 1 + 2)
        k = 0
        for i in range(rows):
            spacing_x = self.background_rect.width // (columns - 1 + 2)
            columns = columns_in_row[i]
            for j in range(columns):
                y = (i % rows + 1) * spacing_y
                x = (j % columns + 1) * spacing_x
                player = self.__create_player(x, y)
                self.entities[k - number_of_players] = player
                k += 1

    def __create_player(self, x, y):
        return Player(
            x=x,
            y=y,
            width=self.CHARACTER_WIDTH,
            height=self.CHARACTER_HEIGHT,
            speed=self.PLAYER_SPEED)

    def update(self, dt):
        """Advance physics by dt (delta time)."""
        for entity in self.entities:
            entity.move(dt)
        for entity in self.entities:
            entity.collide_stage(self.background_rect)

