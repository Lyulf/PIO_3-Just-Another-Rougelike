from components.component import *

class PlayerComponent(Component):
    awailable_player_ids = [i for i in range(4)]
    def __init__(self, is_current_player, id=None):
        self.is_current_player = is_current_player
        self.player_id = id if id is not None else self.awailable_player_ids.pop(0)