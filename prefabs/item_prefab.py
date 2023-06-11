import ui.spritesheet

from prefabs.prefab import *
from utils.resources import get_sprite



class ItemPrefab(Prefab):

    def __init__(self):
        super().__init__()
        self.sprites = {
            'items': {
                'upgrade': get_sprite("resources/items/upgrade.png", True),
            },
        }

    def create(self, position):
        components = super().create(position)
        rigidbody = RigidbodyComponent(0, collision_type=CollisionType.STATIC)
        self._add_component(components, rigidbody)
        rect = pygame.Rect(0, 0, 50, 50)
        anchor = pygame.Vector2(rect.center)
        sprites = self.sprites['items']
        sprite_sheets = {
            'upgrade': ui.spritesheet.SpriteSheet(sprites['upgrade'], 129, 129, 1, 0.5, False),
        }
        offset = pygame.Vector2(0, 0)
        sprite = ImageSpriteComponent(rect.copy(), anchor.copy(), sprite_sheets, 'upgrade', offset)
        self._add_component(components, sprite)

        return components
