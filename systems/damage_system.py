from systems.system import *
from entities.entity import Entity

class DamageSystem(System):
    def on_fixed_update(self):
        entities = self.entity_manager.get_entities()
        ticks = pygame.time.get_ticks()
        for idx, lhs_entity in enumerate(entities):
            lhs_components = self.component_manager.get_components(lhs_entity, TransformComponent, RectHitboxComponent, HealthComponent, DamageComponent)
            try:
                lhs_transform = lhs_components[TransformComponent]
                lhs_rect_hitbox = lhs_components[RectHitboxComponent]
            except (TypeError, KeyError):
                continue

            for rhs_entity in entities[idx + 1:]:
                rhs_components = self.component_manager.get_components(rhs_entity, TransformComponent, RectHitboxComponent, HealthComponent, DamageComponent)
                try:
                    rhs_transform = rhs_components[TransformComponent]
                    rhs_rect_hitbox = rhs_components[RectHitboxComponent]
                except (TypeError, KeyError):
                    continue

                lhs_rect = lhs_rect_hitbox.rect.move(lhs_transform.position - lhs_rect_hitbox.anchor)
                rhs_rect = rhs_rect_hitbox.rect.move(rhs_transform.position - rhs_rect_hitbox.anchor)
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


    def __do_damage(self, damage_source_entity: Entity, health_component: HealthComponent, damage_component: DamageComponent, current_ticks: int):
        if health_component.entity_type in damage_component.ignore_entity_types:
            return
        if current_ticks >= health_component.last_damage_time_tick + health_component.grace_period:
            health_component.current_health -= damage_component.damage
            health_component.was_hurt = True
            if not damage_component.piercing:
                damage_source_entity.is_alive = False
            health_component.last_damage_time_tick = current_ticks