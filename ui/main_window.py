import pygame

from utils.border import set_border

class MainWindow(object):
    """Wrapper for the main window.

    Handles displaying the window and all of its elements.
    """

    @classmethod
    def __init__(self, window_size, fps):
        pygame.init()
        self.window_size = window_size
        self.fps = fps
        self.screen = None
        self.clock = pygame.time.Clock()

    def show(self):
        """Shows the window."""
        self.screen = pygame.display.set_mode(self.window_size)
        stage = self.screen.get_rect().copy()
        wall_size = pygame.Rect(0, 0, stage.width // 16, stage.height // 8)
        stage.left += wall_size.width
        stage.top += wall_size.height
        stage.width = 13 * stage.width // 16 - 2 * wall_size.width
        stage.height -= 2 * wall_size.height
        set_border(stage)

    def update(self):
        """Displays current frame."""
        pygame.display.flip()
        dt = self.clock.tick(self.fps)
        return dt

    def fill_background(self):
        self.screen.fill('black')

    def close(self):
        """Closes the window."""
        pygame.quit()