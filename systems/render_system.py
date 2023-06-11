from systems.system import *
from systems.user_input_system import *
from ui.floating_button_hint import *

class RenderSystem(System):
    def on_update(self):
        surface = pygame.display.get_surface()
        rects = []
        sprites = []
        hints = []

        camera = None
        for entity in self.entity_manager.get_entities():
            if self.component_manager.get_component(entity, CameraComponent):
                camera = entity
                break
        if camera:
            camera_transform = self.component_manager.get_component(camera, TransformComponent)
        else:
            camera_transform = TransformComponent()

        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(
                entity,
                TransformComponent,
                StageComponent,
                RigidbodyComponent,
                ImageSpriteComponent,
                RectSpriteComponent,
                InteractableArea,
                InteractionHint)
            try:
                transform = components[TransformComponent].projection(camera_transform)
                transform_position = transform.position
            except (TypeError, KeyError):
                continue

            # interpolation
            try:
                rigidbody = components[RigidbodyComponent]
                target_position = transform_position + rigidbody.speed * rigidbody.direction * current_dt() / 1000
                transform_position = transform_position.lerp(target_position, pygame.math.clamp(current_dt() / 50, 0, 1))
            except KeyError:
                pass

            try:
                stage_component = components[StageComponent]
                image_sprite = components[ImageSpriteComponent]
                rect = image_sprite.rect.move(transform_position - image_sprite.anchor)
                image_sprite.current_sprite.animate(surface, rect)
                continue
            except KeyError:
                pass

            try:
                interactable_area = components[InteractableArea]
                interactable_area.draw(surface, transform_position)
                continue
            except KeyError:
                pass

            try:
                interactable_hint = components[InteractionHint]
                if self.systems_manager.get_system(UserInputSystem).enabled:
                    hints.append((interactable_hint, transform_position))
                continue
            except KeyError:
                pass

            try:
                rect_sprite = components[RectSpriteComponent]
                rect = rect_sprite.rect.move(transform_position - rect_sprite.anchor)
                rects.append((rect, rect_sprite.color))
            except KeyError:
                pass

            try:
                rigidbody = components[RigidbodyComponent]
                image_sprite = components[ImageSpriteComponent]
                movement_sprites = filter(None, (image_sprite.sprite_sheets.get(key) for key in ('idle', 'up', 'down', 'left', 'right', 'walk')))
                if image_sprite.current_sprite in movement_sprites:
                    try:
                        if rigidbody.direction.x > 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['right']
                        elif rigidbody.direction.x < 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['left']
                        elif rigidbody.direction.y > 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['down']
                        elif rigidbody.direction.y < 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['up']
                    except KeyError:
                        try:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['walk']
                        except KeyError:
                            pass

                rect = image_sprite.rect.move(transform_position - image_sprite.anchor)
                sprites.append((image_sprite.current_sprite, rect, image_sprite.offset))

                if image_sprite.current_sprite.is_finished:
                    image_sprite.current_sprite.is_finished = False
                    image_sprite.current_sprite = image_sprite.sprite_sheets['idle']
                    image_sprite.current_sprite.synchronize_animation()
            except KeyError:
                pass

        for rect, color in sorted(rects, key=lambda x: x[0].y):
            pygame.draw.rect(surface, color, rect)

        for current_sprite, rect, offset in sorted(sprites, key=lambda x: x[1].y):
            current_sprite.animate(surface, rect, *offset) # Animate and draw the image_sprite

        for hint, position in hints:
            hint.draw(surface, position)

