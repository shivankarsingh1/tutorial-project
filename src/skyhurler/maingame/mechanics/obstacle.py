import pygame

from skyhurler.maingame.mechanics.materials import MATERIALS


class Obstacle:

    def __init__(self, rect, material):
        self.rect = pygame.Rect(rect)
        self.material = material
        self.damage = 0.0
        self.destroyed = False
        self.role = None

    @property
    def restitution(self):
        return self.material.restitution

    @property
    def friction(self):
        return self.material.friction

    @property
    def center(self):
        return pygame.Vector2(self.rect.center)

    def take_damage(self, amount):
        if self.destroyed:
            return False
        self.damage += amount
        if self.damage >= self.material.strength:
            self.destroyed = True
            return True
        return False

    def draw(self, surface, theme):
        if self.destroyed:
            return
        color = self.material.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, theme.panel_border, self.rect, 2)
        if self.damage > 0:
            crack = min(255, int(255 * self.damage / self.material.strength))
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((20, 20, 20, crack // 3))
            surface.blit(overlay, self.rect.topleft)
