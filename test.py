import pickle
import pygame

surface = pygame.surface.Surface((500, 500))
data = pickle.dumps(surface)
surface2 = pickle.loads(data)
print(surface2)

rect = pygame.Rect(0, 0, 500, 500)
data = pickle.dumps(rect)
rect2 = pickle.loads(data)
print(rect2)