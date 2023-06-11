import pygame

__loaded_sprites = {}
__loaded_sprites_alpha = {}

def get_sprite(image_path, use_alpha):
    global __loaded_sprites, __loaded_sprites_alpha
    if use_alpha:
        return __loaded_sprites_alpha.setdefault(
            image_path, 
            pygame.image.load(image_path).convert_alpha())
    else:
        return __loaded_sprites.setdefault(
            image_path, 
            pygame.image.load(image_path).convert())