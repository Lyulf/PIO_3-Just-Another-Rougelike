import ui.spritesheet

from prefabs.prefab import *
from utils.resources import get_sprite

class DemonPrefab(Prefab):
    SPEED = 200
    WIDTH = 50
    HEIGHT = 50

    def __init__(self):
        super().__init__()
        self.sprites = {
            'demon': {
                'idle_sprite': get_sprite("resources/enemies/demon/idle.png", True),
                'walk_sprite': get_sprite("resources/enemies/demon/walk.png", True),
                'hurt_sprite': get_sprite("resources/enemies/demon/hurt.png", True),

                'attack_sprite': get_sprite("resources/enemies/demon/attack.png", True),
                'death_sprite': get_sprite("resources/enemies/demon/death.png", True),
            },
        }

    def create(self, position):
        components = super().create(position)
        rigidbody = RigidbodyComponent(self.SPEED)
        self._add_component(components, rigidbody)
        rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        anchor = pygame.Vector2(rect.center)
        rect_hitbox = RectHitboxComponent(rect, anchor, EntityType.ENEMY, [EntityType.PLAYER])
        self._add_component(components, rect_hitbox)
        sprites = self.sprites['demon']
        sprite_sheets = {
            'idle' : ui.spritesheet.SpriteSheet(sprites['idle_sprite'], 256, 256, 350, 1, False),
            'walk' : ui.spritesheet.SpriteSheet(sprites['walk_sprite'], 256, 256, 100, 1, False),
            'hurt' : ui.spritesheet.SpriteSheet(sprites['hurt_sprite'], 256, 256, 100, 1, False),
            'attack' : ui.spritesheet.SpriteSheet(sprites['attack_sprite'], 256, 256, 100, 1, False),
            'death' : ui.spritesheet.SpriteSheet(sprites['death_sprite'], 256, 256, 100, 1, False),
        }
        offset = pygame.Vector2(34, -50)
        sprite = ImageSpriteComponent(rect.copy(), anchor.copy(), sprite_sheets, 'idle', offset)
        self._add_component(components, sprite)
        health = HealthComponent(10, EntityType.ENEMY, 0.1)
        self._add_component(components, health)
        enemy_ai = EnemyAiComponent(AiType.BASIC)
        self._add_component(components, enemy_ai)
        damage = DamageComponent(1, True, [EntityType.ENEMY])
        self._add_component(components, damage)
        return components