from systems.system import *

class MovementSystem(System):
    def on_fixed_update(self):
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, TransformComponent, RigidbodyComponent)
            try:
                transform = components[TransformComponent]
                rigidbody = components[RigidbodyComponent]
            except (KeyError, TypeError):
                continue
            transform.position += rigidbody.direction * rigidbody.speed * current_dt() / 1000

        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, TransformComponent, InteractionHint)
            try:
                transform = components[TransformComponent]
                hint_component = components[InteractionHint]
            except (KeyError, TypeError):
                continue
            try:
                owner_transform = self.component_manager.get_component(hint_component.owner, TransformComponent)
                transform.position = owner_transform.position + hint_component.OFFSET
            except (AttributeError):
                entity.is_alive = False