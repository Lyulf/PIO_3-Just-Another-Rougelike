from uuid import uuid4

class Entitiy(object):
    """Base class for all entities."""

    def __init__(self):
        self.uuid = uuid4()

    def render(self, surface, layer):
        """Method responsible for displaying the entity.
        
        Will be overwritten by child classes."""
        pass
