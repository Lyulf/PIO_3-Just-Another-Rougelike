from engine.game_engine import GameEngine
from entities import *
from ui.main_window import MainWindow
from utils.errors.user_error import UserError
from utils.layers import Layers
from components.player_component import PlayerComponent
from components.transform_component import TransformComponent
from components.interaction_hint_component import InteractionHint
from systems.user_input_system import UserInputSystem
from utils.delta_time import *

import pygame
import sys

class Client(object):
    """Class handling all gameplay logic."""
    def __init__(self, width, height, fps, custom_keys, is_multiplayer=False):
        pygame.init()
        window_size = (width, height)
        self.window = MainWindow(window_size=window_size)
        self.engine = GameEngine(window_size=window_size, fps=fps, keyboard_controls=custom_keys)
        self.__running = False
        self.custom_keys = custom_keys
        self.is_multiplayer = is_multiplayer

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
        self.engine.add_player(keyboard_buttons=self.custom_keys)

        if self.is_multiplayer:
            for joystick_id in range(pygame.joystick.get_count()):
                self.engine.add_player(joystick=pygame.joystick.Joystick(joystick_id))

        self.engine.create()

    def loop(self):
        """Gameplay loop."""
        self.input()
        self.update()

    def input(self):
        """Handles user input."""
        user_inputs_system = self.engine.system_manager.get_system(UserInputSystem)
        keys_down = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                return
            if event.type == pygame.KEYDOWN:
                keys_down.append(event.key)
            elif self.is_multiplayer and event.type == pygame.JOYDEVICEADDED:
                self.engine.add_player(joystick=pygame.joystick.Joystick(event.device_index))
            elif event.type == pygame.JOYBUTTONDOWN:
                keys_down.append(event.button)

        keys = pygame.key.get_pressed()
        user_inputs_system.held_keys = keys
        user_inputs_system.keys_down.extend(keys_down)

    def update(self):
        """Calls on_update in systems"""
        self.engine.update()
        dt = self.window.update()
        update_dt(current_dt() + dt)

    def shutdown(self):
        """Shutdown after gameplay loop."""
        self.engine.destroy()
        self.window.close()
        pygame.quit()
        sys.exit()

    def stop(self):
        """Stops the gameplay loop if it is running."""
        self.__running = False
