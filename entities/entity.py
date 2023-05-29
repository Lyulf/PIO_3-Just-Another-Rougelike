from uuid import uuid4

class Entity(object):
    """Base class for all entities."""

    def __init__(self):
        self.uuid = uuid4()

    def render(self, surface, layer):
        """Method responsible for displaying the entity.
        
        Will be overwritten by child classes."""
        pass

    def move(dt):
        """Moves the entity by in time by dt (delta time).

        Will be overwritten by child classes."""
        pass

    def collide_stage(stage_rect):
        """Collides the entity with the stage.
        
        Behaviour is decided by child classes that overwritte this method."""
        pass
