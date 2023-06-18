import pygame

from systems.system import *
from entities.entity import Entity

class DamageSystem(System):
    def on_fixed_update(self):
        entities = self.entity_manager.get_entities()
        ticks = pygame.time.get_ticks()
        for idx, lhs_entity in enumerate(entities):
            lhs_components = self.component_manager.get_components(
                lhs_entity, TransformComponent, RigidbodyComponent, RectHitboxComponent, HealthComponent, DamageComponent)
            try:
                lhs_transform = lhs_components[TransformComponent]
                lhs_rect_hitbox = lhs_components[RectHitboxComponent]
            except (TypeError, KeyError):
                continue

            for rhs_entity in entities[idx + 1:]:
                rhs_components = self.component_manager.get_components(
                    rhs_entity, TransformComponent, RigidbodyComponent, RectHitboxComponent, HealthComponent, DamageComponent)
                try:
                    rhs_transform = rhs_components[TransformComponent]
                    rhs_rect_hitbox = rhs_components[RectHitboxComponent]
                except (TypeError, KeyError):
                    continue

                lhs_position = lhs_transform.position - lhs_rect_hitbox.anchor
                rhs_position = rhs_transform.position - rhs_rect_hitbox.anchor

                try:
                    lhs_rigidbody = lhs_components[RigidbodyComponent]
                except AttributeError:
                    lhs_velocity = pygame.Vector2()
                else:
                    lhs_velocity = lhs_rigidbody.speed * lhs_rigidbody.direction

                try:
                    rhs_rigidbody = rhs_components[RigidbodyComponent]
                except AttributeError:
                    rhs_velocity = pygame.Vector2()
                else:
                    rhs_velocity = rhs_rigidbody.speed * rhs_rigidbody.direction

                lhs_position, rhs_position = self.__find_positions_at_minimum_distance(
                    lhs_position, lhs_velocity, rhs_position, rhs_velocity)

                lhs_rect = lhs_rect_hitbox.rect.move(lhs_position)
                rhs_rect = rhs_rect_hitbox.rect.move(rhs_position)
                if not lhs_rect.colliderect(rhs_rect):
                    continue

                try:
                    lhs_health = lhs_components[HealthComponent]
                    rhs_damage = rhs_components[DamageComponent]
                except KeyError:
                    pass
                else:
                    self.__do_damage(rhs_entity, lhs_health, rhs_damage, ticks)

                try:
                    rhs_health = rhs_components[HealthComponent]
                    lhs_damage = lhs_components[DamageComponent]
                except KeyError:
                    pass
                else:
                    self.__do_damage(lhs_entity, rhs_health, lhs_damage, ticks)

    def __find_positions_at_minimum_distance(self, lhs_position, lhs_velocity, rhs_position, rhs_velocity):
        ms_since_last_fixed_update = 50
        lhs_last_position = lhs_position - ms_since_last_fixed_update * lhs_velocity
        rhs_last_position = rhs_position - ms_since_last_fixed_update * rhs_velocity

        p = lhs_last_position - rhs_last_position
        v = lhs_velocity - rhs_velocity

        # time when vectors are perpendicular (minimum distance between objects)
        try:
            t = -p.dot(v) / v.magnitude_squared()
        except:
            return lhs_position, rhs_position

        t = pygame.math.clamp(t, 0, ms_since_last_fixed_update)

        print(t)

        lhs_position = lhs_last_position + t * lhs_velocity
        rhs_position = rhs_last_position + t * rhs_velocity

        return lhs_position, rhs_position

    def __do_damage(self, damage_source_entity: Entity, health_component: HealthComponent, damage_component: DamageComponent, current_ticks: int):
        if health_component.entity_type in damage_component.ignore_entity_types:
            return
        if current_ticks >= health_component.last_damage_time_tick + health_component.grace_period:
            health_component.current_health -= damage_component.damage
            health_component.was_hurt = True
            if not damage_component.piercing:
                damage_source_entity.is_alive = False
            health_component.last_damage_time_tick = current_ticks