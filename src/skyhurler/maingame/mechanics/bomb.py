import pygame

from skyhurler.core import settings
from skyhurler.maingame.mechanics.materials import Bomb_shell
from skyhurler.maingame.mechanics.obstacle import Obstacle


class Bomb(Obstacle):
    def __init__(self, rect):
        super().__init__(rect, Bomb_shell)
        self.blast_radius = settings.Bomb_blast_radius
        self.blast_damage = settings.Bomb_blast_damage
        self.blast_impulse = settings.Bomb_blast_impulse

    def draw(self, surface, theme):
        if self.destroyed:
            return
        super().draw(surface, theme)
        cx, cy = self.rect.center
        pygame.draw.circle(surface, theme.danger, (cx, cy),
                           max(3, self.rect.width // 5))