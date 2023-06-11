from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from systems.system import System

class SystemManager(object):
    def __init__(self):
        self.systems = {}

    def add_system(self, priority: int, system: 'System'):
        try:
            self.systems[priority].add(system)
        except KeyError:
            self.systems[priority] = set([system])

    def get_system(self, system_type: type):
        for _, systems in sorted(self.systems.items()):
            for system in systems:
                if isinstance(system, system_type):
                    return system

    def get_systems(self):
        for _, systems in sorted(self.systems.items()):
            for system in systems:
                yield system

    def remove_system(self, priority: int, system: 'System'):
        try:
            self.systems[priority][system]
        except KeyError:
            pass