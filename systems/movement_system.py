from systems.system import *

class MovementSystem(System):
    def on_update(self):
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(entity, TransformComponent, RigidbodyComponent)
            try:
                transform = components[TransformComponent]
                rigidbody = components[RigidbodyComponent]
            except (KeyError, TypeError):
                continue
            transform.position += rigidbody.direction * rigidbody.speed * current_dt()