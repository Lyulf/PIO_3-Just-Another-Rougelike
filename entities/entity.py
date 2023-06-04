
class Entity(object):
    def __init__(self, id):
        self.id = id
        self.is_alive = True # Whether entity shouldn't be garbage collected
