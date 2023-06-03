import math
import pygame
import time
from entity import Entity
from client import *
from ui.main_window import *

class RectEntity(Entity):
    """Base class for humanoid entities."""

    def __init__(self, x, y, width, height, speed, hp=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = pygame.Vector2()
        self.x = x
        self.hp = hp

    def move(self, dt):
        """Moves the character in time by dt (delta time)."""
        offset = dt * self.speed * self.direction
        self.rect.move_ip(offset.x, offset.y)

    def shoot(self):
        self.rect.x += self.speed

    def collide_stage(self, stage_rect):
        """Moves the player back in bounds of the stage."""
        if self.rect.left <= (stage_rect.left + 0.077*stage_rect.width):
            self.rect.left = (stage_rect.left + 0.077*stage_rect.width)
        elif self.rect.right >= (stage_rect.right - 0.2645*stage_rect.width):
            self.rect.right = (stage_rect.right - 0.2645*stage_rect.width)
        if self.rect.top <= (stage_rect.top + 0.125*stage_rect.height):
            self.rect.top = (stage_rect.top + 0.125*stage_rect.height)
        elif self.rect.bottom >= (stage_rect.bottom - 0.125*stage_rect.height):
            self.rect.bottom = (stage_rect.bottom - 0.125*stage_rect.height)


    def search_for_impact(self, projectile, character, projectiles):
            if projectile.rect.colliderect(character.rect):
                projectiles.remove(projectile)
                character.change_animation('hurt')
                character.get_hurt(1, character)

    def collide_with_map(self, projectile, projectiles, stage_rect):
        if projectile.rect.x <= (stage_rect.left + 0.077*stage_rect.width):
            projectiles.remove(projectile)
        elif projectile.rect.x >= (stage_rect.right - 0.2645*stage_rect.width):
            projectiles.remove(projectile)

        """ Do dodania jak bedzie mozna strzelac we wszystkie strony """
        # if projectile.rect.y <= (stage_rect.top + 0.125*stage_rect.height):
        #     projectiles.remove(projectile)
        # elif projectile.rect.y >= (stage_rect.bottom - 0.125*stage_rect.height):
        #     projectiles.remove(projectile)
