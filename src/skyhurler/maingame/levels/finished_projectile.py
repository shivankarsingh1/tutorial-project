import pygame

from skyhurler.core import settings


class FinishedProjectile:

    def __init__(self, projectile):
        self.projectile = projectile
        self.timer = settings.Spent_projectile_lifetime

    def tick(self, dt):
        self.timer = max(0.0, self.timer - dt)

    @property
    def visible(self):
        return self.timer > 0.0

    def draw(self, surface, theme):
        fraction = self.timer / settings.Spent_projectile_lifetime
        centre = (int(self.projectile.position.x),
                  int(self.projectile.position.y))
        if self.projectile.sprite is None:
            radius = max(2, int(self.projectile.radius * fraction))
            pygame.draw.circle(surface, self.projectile.character.color,
                               centre, radius)
            return
        image = self.projectile.scaled_sprite().copy()
        image.set_alpha(int(255 * fraction))
        surface.blit(image, image.get_rect(center=centre))
