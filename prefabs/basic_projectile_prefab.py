from prefabs.prefab import *
        
class BasicProjectilePrefab(Prefab):

    def __init__(self, color):
        super().__init__()
        self.color = color

    def create(self, position):
        components = super().create(position)
        rigidbody = RigidbodyComponent(
            3,
            CollisionType.KINETIC,
        )
        self._add_component(components, rigidbody)
        rect = pygame.Rect(0, 0, 20, 20)
        anchor = pygame.Vector2(rect.center)
        rect_hitbox = RectHitboxComponent(
            rect, anchor, EntityType.PROJECTILE
        )
        self._add_component(components, rect_hitbox)
        rect_sprite = RectSpriteComponent(rect, anchor, self.color)
        self._add_component(components, rect_sprite)
        damage = DamageComponent(1, False, [EntityType.PROJECTILE])
        self._add_component(components, damage)

        return components