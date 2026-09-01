
from abc import ABC, abstractmethod


class Scene(ABC):
    """base class that every screen in the game inherits from"""

    def __init__(self, context):
        self.context = context

    def enter(self):
        """called when the scene becomes the active one, set the scene up in here"""

    def exit(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        """gets passed events from the game loop to deal with"""

    @abstractmethod
    def update(self, dt):
        """called every frame, dt is the time since the last frame in seconds"""

    @abstractmethod
    def draw(self, surface):
        """draw the scene onto the surface given"""
