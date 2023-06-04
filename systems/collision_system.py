from systems.system import *
from utils.border import get_border

class CollisionSystem(System):
    def on_update(self):
        for lhs_idx, lhs_entity in enumerate(self.entity_manager.get_entities()):
            lhs_components = self.component_manager.get_components(
                lhs_entity, TransformComponent, RigidbodyComponent, RectHitboxComponent, HealthComponent, DamageComponent)
            try:
                self.__collide_border(lhs_entity, lhs_components)
                if not lhs_entity.is_alive:
                    continue
            except (TypeError, KeyError):
                continue
            for rhs_entity in self.entity_manager.get_entities()[lhs_idx + 1:]:
                rhs_components = self.component_manager.get_components(
                    rhs_entity, TransformComponent, RigidbodyComponent, RectHitboxComponent, HealthComponent, DamageComponent)
                try:
                    self.__collide_entity(lhs_entity, lhs_components, rhs_entity, rhs_components)
                except (TypeError, KeyError):
                    continue

    def __collide_border(self, entity, components):
        transform = components[TransformComponent]
        rigidbody = components[RigidbodyComponent]
        rect_hitbox = components[RectHitboxComponent]
        if rigidbody.collision_type == CollisionType.NONE:
            raise TypeError()
        if rigidbody.collision_type == CollisionType.STATIC:
            return
        surface = pygame.display.get_surface()
        border = get_border()
        rect = rect_hitbox.rect.move(transform.position - rect_hitbox.anchor)
        new_rect = rect.clamp(border)
        delta_position = pygame.Vector2(new_rect.center) - pygame.Vector2(rect.center)
        if rect_hitbox.entity_type == EntityTypes.PROJECTILE and any(delta_position):
            entity.is_alive = False
            return
        transform.position += delta_position


        # if rect.left <= border.left:
        #     transform.position.x += border.left - rect.left
        # elif rect.right >= border.right:
        #     transform.position.x -=  rect.right - border.right
        #     rect.right = border.right
        # if rect.top <= border.top:
        #     transform.position.y += border.top - rect.top
        # elif rect.bottom >= border.bottom:
        #     transform.position.y -=  rect.bottom - border.bottom

    def __collide_entity(self, lhs_entity, lhs_components, rhs_entity, rhs_components):
        lhs_transform = lhs_components[TransformComponent]
        lhs_rigidbody = lhs_components[RigidbodyComponent]
        lhs_rect_hitbox = lhs_components[RectHitboxComponent]
        rhs_transform = rhs_components[TransformComponent]
        rhs_rigidbody = rhs_components[RigidbodyComponent]
        rhs_rect_hitbox = rhs_components[RectHitboxComponent]
        if lhs_rigidbody.collision_type == CollisionType.STATIC and rhs_rigidbody.collision_type == CollisionType.STATIC:
            raise TypeError()
        if lhs_rigidbody.collision_type == CollisionType.NONE:
            raise TypeError()
        if rhs_rigidbody.collision_type == CollisionType.NONE:
            raise TypeError()
        if lhs_rect_hitbox.entity_type in rhs_rect_hitbox.ignore_types:
            raise TypeError()
        if rhs_rect_hitbox.entity_type in lhs_rect_hitbox.ignore_types:
            raise TypeError()

        lhs_rect = lhs_rect_hitbox.rect.move(lhs_transform.position - lhs_rect_hitbox.anchor)
        rhs_rect = rhs_rect_hitbox.rect.move(rhs_transform.position - rhs_rect_hitbox.anchor)

        overlap_rect = lhs_rect.clip(rhs_rect)
        delta_position = pygame.Vector2(overlap_rect.size)
        try:
            normal_delta_position = delta_position.normalize()
        except ValueError:
            return

        try:
            lhs_health = lhs_components[HealthComponent]
            rhs_damage = rhs_components[DamageComponent]
            lhs_health.current_health -= rhs_damage.damage
            lhs_health.was_hurt = True
            if not rhs_damage.piercing:
                rhs_entity.is_alive = False
                return
        except KeyError:
            pass

        try:
            rhs_health = rhs_components[HealthComponent]
            lhs_damage = lhs_components[DamageComponent]
            rhs_health.current_health -= lhs_damage.damage
            rhs_health.was_hurt = True
            if not lhs_damage.piercing:
                lhs_entity.is_alive = False
                return
        except KeyError:
            pass

        if abs(normal_delta_position.x) > abs(normal_delta_position.y):
            delta_position.x = 0
        elif abs(normal_delta_position.x) < abs(normal_delta_position.y):
            delta_position.y = 0
        
        if lhs_rect.centerx < rhs_rect.centerx:
            delta_position.x = -delta_position.x
        if lhs_rect.centery < rhs_rect.centery:
            delta_position.y = -delta_position.y

        if lhs_rigidbody.collision_type == CollisionType.DYNAMIC and rhs_rigidbody.collision_type == CollisionType.DYNAMIC:
            delta_position //= 2
        if lhs_rigidbody.collision_type == CollisionType.DYNAMIC:
            lhs_transform.position += delta_position
        if rhs_rigidbody.collision_type == CollisionType.DYNAMIC:
            rhs_transform.position -= delta_position
        
