import math

from systems.system import *

class EnemyAiSystem(System):
    def on_fixed_update(self):
        entities = self.entity_manager.get_entities()
        player_positions = []
        for entity in entities:
            components = self.component_manager.get_components(entity, PlayerComponent, TransformComponent)
            try:
                if components.get(PlayerComponent):
                    transform = components[TransformComponent]
                    player_positions.append(transform.position)
            except (TypeError, KeyError):
                continue

        for entity in entities:
            components = self.component_manager.get_components(entity, TransformComponent, RigidbodyComponent, EnemyAiComponent)
            try:
                ai_component = components[EnemyAiComponent]
                rigidbody_component = components[RigidbodyComponent]
                transform = components[TransformComponent]
            except (TypeError, KeyError):
                continue

            if not player_positions:
                rigidbody_component.direction = pygame.Vector2()
                continue

            if ai_component.ai_type == AiType.BASIC:
                player_position = self.__find_closest_player(transform.position, player_positions)
                player_delta_position = player_position - transform.position
                try:
                    # Tries to only go horizontally or vertically
                    direction = player_delta_position.normalize()
                    if abs(direction.x) >= abs(direction.y):
                        direction.y = 0
                    else:
                        direction.x = 0
                    rigidbody_component.direction = direction.normalize()
                except ValueError:
                    rigidbody_component.direction = pygame.Vector2()

    def __find_closest_player(self, position, player_positions):
        last_distance = math.inf
        selected_player = None
        for player_position in player_positions:
            delta_distance = position - player_position
            delta_distance = delta_distance.magnitude_squared()
            if delta_distance < last_distance:
                last_distance = delta_distance
                selected_player = player_position
        return selected_player
