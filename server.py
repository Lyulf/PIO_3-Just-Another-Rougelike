from engine.game_engine import GameEngine

import asyncio
import cmd
import pygame
import socket
import sys
import threading
import time


class Server(object):
    DEFAULT_PORT=9999
    WIDTH = 1280
    HEIGHT = 720
    """Server that synchronizes game engines between clients."""
    def __init__(self, port=DEFAULT_PORT, max_players=4):
        self.port = port
        self.max_players = max_players
        self.__running = False
        self.clients = []
        self.event_loop = None
        self.engine = GameEngine()
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.engine.set_background_rect(self.rect)

    def start(self):
        """Starts server loops"""
        thread = threading.Thread(target=self.run)
        thread.start()
        return thread

    def run(self):
        """Runs server loop"""
        assert(not self.__running)
        self.__running = True
        try:
            try:
                self.event_loop = asyncio.get_running_loop()
            except RuntimeError:
                self.event_loop = asyncio.new_event_loop()
            main_task = self.event_loop.create_task(self.main_loop())
            self.event_loop.run_until_complete(main_task)
        except Exception:
            self.__running = False
            raise

    async def main_loop(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.setblocking(False)
        try:
            server_socket.listen(self.max_players)

            self.event_loop.create_task(self.engine_loop())
            while self.__running:
                try:
                    client_socket, _ = server_socket.accept()
                    self.event_loop.create_task(self.handle_client(client_socket))
                except BlockingIOError:
                    await asyncio.sleep(1)
            while self.clients:
                await asyncio.sleep(1)
        finally:
            server_socket.close()

    async def engine_loop(self):
        """Updates engine physics in a loop"""
        dt = 0
        last_time = self.get_time_ms()
        while self.__running:
            self.engine.update(dt)
            await asyncio.sleep(0.02)
            new_time = self.get_time_ms()
            dt = new_time - last_time
            last_time = new_time

    def get_time_ms(self):
        """Gets time in ms"""
        return time.monotonic_ns() * 1000000

    async def handle_client(self, client_socket):
        """Handles client."""
        self.clients.append(client_socket)
        try:
            print("Sending state")
            self.engine.send_current_state(client_socket)
            print("Assigning player")
            self.engine.assign_player(client_socket)
            while self.__running:
                print("Synchronizing player")
                await self.synchronize_client_engine(client_socket)
            # await loop.sock_sendall()
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    async def receive_client_events(self, client_socket):
        """Receives events from client."""
        while self.__running:
            await asyncio.sleep(1)
            #await loop.sock_recv()

    async def synchronize_client_engine(self, client_socket):
        """Synchronizes entities between server engine and client engine."""
        self.engine.synchronize_with_client(client_socket)

    def stop(self):
        """Stops the server."""
        self.__running = False

class ServerShell(cmd.Cmd):
    prompt = '(server) '

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.server = None
        self.thread = None

    def __enter__(self):
        self.server = Server(port=self.port)
        self.thread = self.server.start()
        print(f"Server started at port {self.port}. Type help or ? for list of commands.\n")
        return self

    def __exit__(self, *exception_args):
        print("\nClosing server...")
        self.server.stop()
        self.thread.join()
        print("Server closed.")

    def do_get_port(self, arg):
        """Displays the port of current server."""
        print(f"port = {self.port}")
    
    def do_exit(self, arg):
        """Stops the server."""
        return True

if __name__ == '__main__':
    import argparse

    command_line_parser = argparse.ArgumentParser(
        description="Starts the server",
    )

    command_line_parser.add_argument('-p', '--port', default=Server.DEFAULT_PORT, type=int, help="Port used by the server")

    parsed_args = vars(command_line_parser.parse_args())

    with ServerShell(**parsed_args) as shell:
        shell.cmdloop()
