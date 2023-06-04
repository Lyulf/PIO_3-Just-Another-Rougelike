from engine.game_engine import GameEngine
from entities import *
from ui.main_window import MainWindow
from utils.errors.user_error import UserError
from utils.layers import Layers
from components.controls_component import Controls, ControlsComponent
from components.player_component import PlayerComponent
from systems.user_input_system import UserInputSystem
from utils.delta_time import *

import pygame
import socket
import sys

class Client(object):
    """Class handling all gameplay logic."""
    def __init__(self, width, height, fps, custom_keys, ip=None, port=None):
        pygame.init()
        self.window = MainWindow(size=(width, height), fps=fps)
        self.engine = GameEngine()
        self.player = None
        self.__running = False
        self.custom_keys = custom_keys
        self.ip = ip
        self.port = port

    def run(self):
        """Starts the game."""
        if self.__running:
            raise UserError('Game is already running')
        self.__running = True

        self.init()
        while self.__running:
            self.loop()
        self.shutdown()

    def init(self):
        """Initialization before gameplay loop."""
        self.window.show()
        self.engine.load_images()
        self.player = self.engine.spawn_players(1)[0]
        self.engine.spawn_opponents(2)
        controls = ControlsComponent(self.custom_keys)
        self.engine.component_manager.add_component(self.player, controls)
        player_component = self.engine.component_manager.get_component(self.player, PlayerComponent)
        player_component.is_current_player = True

        self.engine.create()

    def loop(self):
        """Gameplay loop."""
        self.input()
        self.update()

    def input(self):
        """Handles user input."""
        user_inputs_system = self.engine.system_manager.get_system(UserInputSystem)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                return
        keys = pygame.key.get_pressed()
        user_inputs_system.held_keys = keys

    def update(self):
        """Calls on_update in systems"""
        self.window.fill_background()
        self.engine.update()
        dt = self.window.update()
        update_dt(dt)

    def shutdown(self):
        """Shutdown after gameplay loop."""
        self.engine.destroy()
        self.window.close()
        pygame.quit()
        sys.exit()

    def stop(self):
        """Stops the gameplay loop if it is running."""
        self.__running = False
