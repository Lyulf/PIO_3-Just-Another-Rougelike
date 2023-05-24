from widget import Widget

import pygame

class MainWindow(Widget):
    """Wrapper for the main window.

    Handles displaying the window and all of its elements.
    """
    def __init__(self, position, size, fps, parent=None):
        pygame.init()
        super().__init__(position=position, size=size, parent=parent)

        self.fps = fps

        self.screen = None
        self.clock = pygame.time.Clock()

    def show(self):
        """Shows the window"""
        self.screen = pygame.display.set_mode(self.size)

    def update(self):
        """Displays current frame"""
        self.render()

        for child in self.children.values():
            child.render()

        pygame.display.flip()
        dt = self.clock.tick(self.fps)
        return dt

    def render(self):
        """Renders only the window background"""
        self.screen.fill('blue')

    def close(self):
        """Closes the window"""
        pygame.quit()