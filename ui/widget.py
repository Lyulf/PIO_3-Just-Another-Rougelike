import uuid

class Widget(object):
    """Base class for UI components."""
    def __init__(self, position, size, parent=None):
        self.parent = parent
        self.position = position
        self.size = size
        self.children = {}
        try:
            self.uuid = self.parent.add_widget(self)
        except AttributeError:
            self.uuid = None

    def add_widget(self, widget):
        """Adds child widget to current widget"""
        uuid = uuid.uuid4()
        self.children[uuid] = widget
        widget.parent = self
        widget.uuid = uuid
