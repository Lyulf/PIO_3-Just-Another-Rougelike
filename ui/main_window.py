import pygame



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

    def update(self):
        """Displays current frame."""
        pygame.display.flip()
        dt = self.clock.tick(self.fps)
        return dt

    def fill_background(self):
        image = self.scaled_image
        self.screen.blit(image, (0, 0))

    def close(self):
        """Closes the window."""
        pygame.quit()