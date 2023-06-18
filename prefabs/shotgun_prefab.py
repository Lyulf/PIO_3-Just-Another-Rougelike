import ui.spritesheet

from prefabs.prefab import *
from utils.resources import get_sprite
from entities.entity import Entity
from components.health_component import HealthComponent
from components.weapon_component import WeaponComponent
from components.weapon_component import WeaponType


class ShotgunPrefab(Prefab):

    def __init__(self):
        super().__init__()
        self.sprites = {
            'items': {
                'upgrade': get_sprite("resources/items/shotgun.png", True),
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
        item_component = ItemComponent()
        self._add_component(components, item_component)
        interaction_component = InteractionComponent(rect, anchor, self.pick_up_item)
        self._add_component(components, interaction_component)
        return components
    def pick_up_item(self, player_entity, item_entity):
        item_entity.is_alive = False
        components = self.component_manager.get_components(player_entity, WeaponComponent)
        try:
            gun = components[WeaponComponent]
        except (TypeError, KeyError):
            return
        gun.weapon_type = WeaponType.SHOTGUN
        gun.projectile_count = 1
        gun.spread_angle = 50
        gun.fire_delay = 100
