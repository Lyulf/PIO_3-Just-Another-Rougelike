from prefabs.prefab import *
from ui.spritesheet import SpriteSheet
from utils.resources import get_sprite

import random

class PlayerPrefab(Prefab):
    SPEED = 1
    WIDTH = 50
    HEIGHT = 50
    COLOR = pygame.Color(246, 187, 148)
    SPRITE_OFFSET = pygame.Vector2(0, -50)
    GRACE_PERIOD = 0.2

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.old_color = self.COLOR
        self.new_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.sprites = {
            'player': {
                'idle_sprite': get_sprite("resources/playerModel/idle.png", False),
                'left_sprite': get_sprite("resources/playerModel/left.png", False),
                'right_sprite': get_sprite("resources/playerModel/right.png", False),
                'down_sprite': get_sprite("resources/playerModel/down.png", False),
                'up_sprite': get_sprite("resources/playerModel/up.png", False),
                'hurt_sprite': get_sprite("resources/playerModel/hurt.png", False),
                'death_sprite': get_sprite("resources/playerModel/death.png", False),
            },
            'health_bar': [
                get_sprite(f"resources/HP_Bar/{id}.png", False) for id in range(11)
            ]
        }

    def create(self, position):
        components = super().create(position)

        rigidbody = RigidbodyComponent(self.SPEED)
        self._add_component(components, rigidbody)

        player_rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        anchor = pygame.Vector2(player_rect.center)

        rect_hitbox = RectHitboxComponent(player_rect, anchor, EntityType.PLAYER, [EntityType.PLAYER])
        self._add_component(components, rect_hitbox)

        sprites = self.sprites['player']

        sprite_sheets = {
            'idle': SpriteSheet(sprites['idle_sprite'], 16, 16, 500, 6, True, self.old_color, self.new_color),
            'left': SpriteSheet(sprites['left_sprite'], 16, 16, 250, 6, True, self.old_color, self.new_color),
            'right': SpriteSheet(sprites['right_sprite'], 16, 16, 250, 6, True, self.old_color, self.new_color),
            'down': SpriteSheet(sprites['down_sprite'], 16, 16, 250, 6, True, self.old_color, self.new_color),
            'up': SpriteSheet(sprites['up_sprite'], 16, 16, 250, 6, True, self.old_color, self.new_color),
            'death': SpriteSheet(sprites['death_sprite'], 16, 16, 250, 6, True, self.old_color, self.new_color),
            'hurt': SpriteSheet(sprites['hurt_sprite'], 16, 16, 250, 6, True, self.old_color, self.new_color),
        }
        sprite = ImageSpriteComponent(player_rect.copy(), anchor.copy(), sprite_sheets, 'idle', self.SPRITE_OFFSET)
        self._add_component(components, sprite)

        health = HealthComponent(10, EntityType.PLAYER, self.GRACE_PERIOD)
        self._add_component(components, health)

        player_component = PlayerComponent(False, self.id)
        self._add_component(components, player_component)

        sidebar_health_bar = PlayerSidebarHealthBarComponent(self.sprites['health_bar'])
        self._add_component(components, sidebar_health_bar)

        return components
