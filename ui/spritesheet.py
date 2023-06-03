import pygame
import numpy as np
class SpriteSheet:
    def __init__(self, image, sprite_width, sprite_height, animation_speed, scale, random_color=False, old_color=None, new_color=None):
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.animation_speed = animation_speed
        self.scale = scale
        self.is_finished = False
        self.random_color = random_color
        self.old_color = old_color
        self.new_color = new_color

        # Load the sprite sheet image
        self.sprite_sheet = image
        if random_color:
            self.sprite_sheet = self.change_color(self.sprite_sheet, self.old_color, self.new_color)
            self.sprite_sheet.set_colorkey('Black')

        # Calculate the number of rows and columns in the sprite sheet
        self.columns = self.sprite_sheet.get_width() // sprite_width
        self.rows = self.sprite_sheet.get_height() // sprite_height

        # Generate a list of sprites from the sprite sheet
        self.sprites = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * sprite_width
                y = row * sprite_height
                rect = pygame.Rect(x, y, sprite_width, sprite_height)
                self.sprites.append(self.sprite_sheet.subsurface(rect))

        self.current_frame = 0

    def animate(self, surface, rect, offset_x=0, offset_y=0):
        current_time = pygame.time.get_ticks()

        # Update the current frame if enough time has passed

        self.current_frame = (current_time // self.animation_speed) % len(self.sprites)
        if self.current_frame + 1 == len(self.sprites):
            self.is_finished = True

        sprite_x = rect.x - (self.sprite_width * self.scale - rect.width) / 2 + offset_x
        sprite_y = rect.y - (self.sprite_height * self.scale - rect.height) / 2 + offset_y

        # Scale the sprite to the desired size
        sprite = pygame.transform.scale(self.sprites[self.current_frame],
                                        (self.sprite_width * self.scale, self.sprite_height * self.scale))

        # Draw the sprite on the surface at the given position
        surface.blit(sprite, (sprite_x, sprite_y))

    def change_color(self, image, old_color, new_color):
        """Change a specific color in an image to a new color."""
        width, height = image.get_size()

        # Convert the image to a NumPy array
        pixel_array = pygame.surfarray.array3d(image)

        # Convert the color values to NumPy arrays
        old_color_array = np.array([old_color.r, old_color.g, old_color.b])
        new_color_array = np.array([new_color.r, new_color.g, new_color.b])

        # Find the pixels with the old color
        mask = np.all(pixel_array == old_color_array, axis=-1)

        # Replace the old color with the new color
        pixel_array = np.where(mask[..., np.newaxis], new_color_array, pixel_array)

        # Convert the NumPy array back to a Surface
        modified_image = pygame.surfarray.make_surface(pixel_array)

        return modified_image
