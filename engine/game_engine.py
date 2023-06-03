import pygame
import math

from entities import *

class GameEngine(object):
    """Class handling game physics."""
    CHARACTER_WIDTH = 50
    CHARACTER_HEIGHT = 100
    OPPONENT_WIDTH = 40
    OPPONENT_HEIGHT = 80
    OPPONENT_SPEED = 1
    PLAYER_SPEED = 1

    def __init__(self):
        self.entities = []
        self.projectiles = []
        self.background_rect = None

    def set_background_rect(self, rect):
        """Sets background rectangle.

        It should be windows rectangle or map rectangle."""
        self.background_rect = rect

    def draw_healthbar(self, screen, x, y, width, height):
        healthbar_img = pygame.image.load("resources/HP_Bar/0.png")
        if self.entities[0].hp == 10:
            healthbar_img = pygame.image.load("resources/HP_Bar/10.png")
        elif self.entities[0].hp == 9:
            healthbar_img = pygame.image.load("resources/HP_Bar/9.png")
        elif self.entities[0].hp == 8:
            healthbar_img = pygame.image.load("resources/HP_Bar/8.png")
        elif self.entities[0].hp == 7:
            healthbar_img = pygame.image.load("resources/HP_Bar/7.png")
        elif self.entities[0].hp == 6:
            healthbar_img = pygame.image.load("resources/HP_Bar/6.png")
        elif self.entities[0].hp == 5:
            healthbar_img = pygame.image.load("resources/HP_Bar/5.png")
        elif self.entities[0].hp == 4:
            healthbar_img = pygame.image.load("resources/HP_Bar/4.png")
        elif self.entities[0].hp == 3:
            healthbar_img = pygame.image.load("resources/HP_Bar/3.png")
        elif self.entities[0].hp == 2:
            healthbar_img = pygame.image.load("resources/HP_Bar/2.png")
        elif self.entities[0].hp == 1:
            healthbar_img = pygame.image.load("resources/HP_Bar/1.png")
        elif self.entities[0].hp == 0:
            healthbar_img = pygame.image.load("resources/HP_Bar/0.png")
        healthbar_img = pygame.transform.scale(healthbar_img, (width, height))
        screen.blit(healthbar_img, (x, y))

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
    def spawn_opponents(self, number_of_opponents):
        """Spawns opponents evenly distributed around the whole map."""
        self.entities += [None] * number_of_opponents
        rows = math.floor(math.sqrt(number_of_opponents))
        columns = math.ceil(number_of_opponents / rows)
        last_column = math.floor(number_of_opponents / rows)
        columns_in_row = [columns if row != rows - 1 else last_column for row in range(rows)]
        spacing_y = self.background_rect.height // (rows - 1 + 2)
        k = 0
        for i in range(rows):
            spacing_x = self.background_rect.width // (columns - 1 + 2)
            columns = columns_in_row[i]
            for j in range(columns):
                y = (i % rows + 1) * spacing_y
                x = (j % columns + 1) * spacing_x
                opponent = self.__create_opponent(x, y)
                self.entities[k - number_of_opponents] = opponent
                k += 1

    def __create_player(self, x, y):
        return Player(
            x=x,
            y=y,
            width=self.CHARACTER_WIDTH,
            height=self.CHARACTER_HEIGHT,
            speed=self.PLAYER_SPEED,
            hp=10)

    def __create_opponent(self, x, y):
        return Opponent(
            x=x,
            y=y,
            width=self.OPPONENT_WIDTH,
            height=self.OPPONENT_HEIGHT,
            speed=self.OPPONENT_SPEED,
            hp=10)

    def update(self, dt):
        """Advance physics by dt (delta time)."""
        for entity in self.entities:
            entity.move(dt)
        for entity in self.entities:
            entity.collide_stage(self.background_rect)
        for projectile in self.projectiles:
            projectile.shoot() 
            projectile.collide_with_map(projectile, self.projectiles, self.background_rect)
            for character in self.entities:
                character.search_for_impact(projectile, character, self.projectiles)
        for character in self.entities:
            if character.hp == -1:
                self.entities.remove(character)


