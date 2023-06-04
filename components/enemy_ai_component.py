from components.component import Component
from enum import Enum

class AiType(Enum):
    BASIC = 0

class EnemyAiComponent(Component):
    def __init__(self, ai_type: AiType):
        self.ai_type = ai_type