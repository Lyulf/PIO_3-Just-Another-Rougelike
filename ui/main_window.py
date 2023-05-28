import pygame

class MainWindow(object):
    """Wrapper for the main window.

    Handles displaying the window and all of its elements.
    """
    def __init__(self, size, fps):
        pygame.init()
        self.size = size
        self.fps = fps

        self.screen = None
        self.clock = pygame.time.Clock()

    def show(self):
        """Shows the window."""
        self.screen = pygame.display.set_mode(self.size)

    def update(self):
        """Displays current frame."""
        pygame.display.flip()
        dt = self.clock.tick(self.fps)
        return dt

    def fill_background(self):
        """Fills the background with color."""
        self.screen.fill('blue')

    def close(self):
        """Closes the window."""
        pygame.quit()