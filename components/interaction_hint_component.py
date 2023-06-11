from components.component import *
from ui.floating_button_hint import *

class InteractionHint(Component):
    OFFSET = pygame.Vector2(0, -120)

    def __init__(self, owner, button, visible = False):
        self.owner = owner
        self.button_hint = FloatingButtonHint(button)
        self.visible = visible

    def draw(self, surface, position):
        if self.visible:
            self.button_hint.draw(surface, position)