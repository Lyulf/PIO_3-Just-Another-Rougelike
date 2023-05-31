from engine.game_engine import GameEngine
from entities import *
from ui.main_window import MainWindow
from utils.errors.user_error import UserError
from utils.layers import Layers

import pygame

class Client(object):
    """Class handling all gameplay logic."""
    def __init__(self, width, height, fps):
        pygame.init()
        self.window = MainWindow(size=(width, height), fps=fps)
        self.engine = GameEngine()
        self.player = None
        self.__running = False
        self.dt = 0

    def run(self):
        """Starts the game."""
        if self.__running:
            raise UserError('Game is already running')
        self.__running = True

        self.init()
        try:
            while self.__running:
                self.loop()
        finally:
            self.shutdown()

    def init(self):
        """Initialization before gameplay loop."""
        self.window.show()
        self.engine.set_background_rect(self.window.screen.get_rect())
        self.engine.spawn_players(4)
        # Will be replaced after server is added.
        self.player = self.engine.entities[0]

    def loop(self):
        """Gameplay loop."""
        self.input()
        self.update()
        self.render()

    def input(self):
        """Handles user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectile = Projectile(self.player.rect.right, self.player.rect.centery, 5, 5, 14)
                    self.engine.entities.append(projectile)
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2()
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        try:
            direction.normalize_ip()
            self.player.direction = direction
        except ValueError:
            self.player.direction = pygame.Vector2()

    def update(self):
        """Handles gameplay logic."""
        self.engine.update(self.dt)

    def render(self):
        """Displays the game."""
        entities = self.engine.entities
        self.window.fill_background()
        for layer in Layers:
            for entitity in entities:
                entitity.render(self.window.screen, layer)
        self.dt = self.window.update()

    def shutdown(self):
        """Shutdown after gameplay loop."""
        self.window.close()

    def stop(self):
        """Stops the gameplay loop if it is running."""
        self.__running = False
