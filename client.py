from engine.game_engine import GameEngine
from entities import *
from ui.main_window import MainWindow
from utils.errors.user_error import UserError
from utils.layers import Layers
from components.controls_component import Controls, ControlsComponent
from systems.user_input_system import UserInputSystem
from utils.delta_time import *

import pygame
import socket
import sys

class Client(object):
    """Class handling all gameplay logic."""
    def __init__(self, width, height, fps, custom_keys, is_multiplayer=False, ip=None, port=None):
        pygame.init()
        self.window = MainWindow(size=(width, height), fps=fps)
        self.engine = GameEngine()
        self.player = None
        self.__running = False
        self.custom_keys = custom_keys
        self.is_multiplayer = is_multiplayer
        self.ip = ip
        self.port = port
        self.socket = None

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
        if self.is_multiplayer:
            self.socket = self.connect_to_server()
        self.window.show()
        self.engine.load_images()
        if self.is_multiplayer:
            print("Receive current state")
            self.engine.receive_current_state(self.socket)
            print("Receive player")
            self.player = self.engine.receive_player(self.socket)
        if not self.is_multiplayer:
            self.player = self.engine.spawn_players(2)[0]
            self.engine.spawn_opponents(1)
        controls = ControlsComponent(self.custom_keys)
        self.engine.component_manager.add_component(self.player, controls)
        self.engine.create()

    def connect_to_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        return sock

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
            elif event.type == pygame.KEYDOWN:
                if event.key == self.custom_keys[Controls.SHOOT]:
                    user_inputs_system.keys_down.append(self.custom_keys[Controls.SHOOT])
        keys = pygame.key.get_pressed()
        user_inputs_system.held_keys = keys

    def update(self):
        """Calls on_update in systems"""
        self.window.fill_background()
        if self.is_multiplayer:
            print("Synchronizing with server")
            self.engine.synchronize_with_server(self.socket)
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
