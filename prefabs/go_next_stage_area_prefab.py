from prefabs.prefab import *
from systems.game_state_system import GameStateSystem

class GoNextStageAreaPrefab(Prefab):
    WIDTH = 320
    HEIGHT = 180
    LINE_OFFSET = pygame.Vector2(0, 200)
    LINE_SPACING = pygame.Vector2(0, 10)

    def __init__(self, color, game_state_system: GameStateSystem):
        super().__init__()
        self.color = color
        self.game_state_system = game_state_system

    def create(self, position):
        components = super().create(position)
        rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        anchor = pygame.Vector2(rect.topleft)
        interactable_area = InteractableArea(rect, anchor, self.go_next, self.color, line_offset=self.LINE_OFFSET, line_spacing=self.LINE_SPACING)
        self._add_component(components, interactable_area)
        return components

    def go_next(self, owner, hint):
        self.game_state_system.go_to_next_stage()