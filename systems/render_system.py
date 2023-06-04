from systems.system import *

class RenderSystem(System):
    def on_update(self):
        surface = pygame.display.get_surface()
        rects = []
        sprites = []
        for entity in self.entity_manager.get_entities():
            components = self.component_manager.get_components(
                entity,
                TransformComponent,
                RigidbodyComponent,
                ImageSpriteComponent,
                RectSpriteComponent)
            try:
                transform = components[TransformComponent]
            except (TypeError, KeyError):
                continue

            try:
                rect_sprite = components[RectSpriteComponent]
                rect = rect_sprite.rect.move(transform.position - rect_sprite.anchor)
                rects.append((rect, rect_sprite.color))
            except KeyError:
                pass

            try:
                rigidbody = components[RigidbodyComponent]
                image_sprite = components[ImageSpriteComponent]
                try:
                    if image_sprite.current_sprite in (image_sprite.sprite_sheets[key] for key in ('idle', 'up', 'down', 'left', 'right')):
                        if rigidbody.direction.x > 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['right']
                        elif rigidbody.direction.x < 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['left']
                        elif rigidbody.direction.y > 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['down']
                        elif rigidbody.direction.y < 0:
                            image_sprite.current_sprite = image_sprite.sprite_sheets['up']
                except KeyError:
                    pass

                rect = image_sprite.rect.move(transform.position - image_sprite.anchor)
                sprites.append((image_sprite.current_sprite, rect, image_sprite.offset))

                if image_sprite.current_sprite.is_finished:
                    image_sprite.current_sprite.is_finished = False
                    image_sprite.current_sprite = image_sprite.sprite_sheets['idle']
            except KeyError:
                pass

        for rect, color in sorted(rects, key=lambda x: x[0].y):
            pygame.draw.rect(surface, color, rect)

        for current_sprite, rect, offset in sorted(sprites, key=lambda x: x[1].y):
            current_sprite.animate(surface, rect, *offset) # Animate and draw the image_sprite

