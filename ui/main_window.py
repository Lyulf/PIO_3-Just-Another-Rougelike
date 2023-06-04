import pygame

from utils.border import set_border

class MainWindow(object):
    """Wrapper for the main window.

    Handles displaying the window and all of its elements.
    """

    is_loaded = False

    @classmethod
    def load_images(cls):
        if not cls.is_loaded:
            cls.is_loaded = True
            cls.map_image = pygame.image.load("resources\Map\plansza.png")
    def __init__(self, size, fps):
        pygame.init()
        self.load_images()
        self.size = size
        self.fps = fps
        self.screen = None
        self.clock = pygame.time.Clock()
        self.scaled_image = pygame.transform.scale(self.map_image, self.size)

    def show(self):
        """Shows the window."""
        self.screen = pygame.display.set_mode(self.size)
        stage = self.screen.get_rect().copy()
        wall_size = pygame.Rect(0, 0, stage.width // 16, stage.height // 8)
        stage.left += wall_size.width
        stage.top += wall_size.height
        stage.width = 3 * stage.width // 4
        stage.width -= wall_size.width
        stage.height -= 2 * wall_size.height
        #stage.height -= wall_size.height
        set_border(stage)

    def update(self):
        """Displays current frame."""
        pygame.display.flip()
        dt = self.clock.tick(self.fps)
        return dt

    def fill_background(self):
        image = self.scaled_image
        self.screen.fill(pygame.Color(43, 42, 41))
        self.screen.blit(image, (0, 0))

    def close(self):
        """Closes the window."""
        pygame.quit()