from engine.game_engine import GameEngine
from entities.player import Player
from ui.main_window import MainWindow
from utils.errors.user_error import UserError
from utils.layers import Layers

import pygame

class Client(object):
    """Class handling all gameplay logic."""
    def __init__(self, width, height, fps):
        pygame.init()
        self.window = MainWindow(position=None, size=(width, height), fps=fps)
        self.engine = GameEngine()
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
        screen = self.window.screen
        x = screen.get_width() // 2
        y = screen.get_height() // 2

        self.engine.entities.append(Player(x - 50, y - 50, 100, 100))

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

    def update(self):
        """Handles gameplay logic."""
        pass

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
