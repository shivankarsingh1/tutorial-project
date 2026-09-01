import pygame

from skyhurler.core import settings
from skyhurler.core.fonts import get_font


class Enemy:
    '''a target for the player to destroy, stands still unless a subclass
    makes it move'''

    def __init__(self, name, position, max_hp, points, radius, color):
        self.name = name
        self.max_hp = max_hp
        self.points = points
        self.radius = radius
        self.color = color
        self.position = pygame.Vector2(position)
        self.hp = max_hp
        self.alive = True
        # obstacle the enemy stands on, it breaks when the enemy dies
        self.platform = None

    def take_damage(self, amount):
        '''does the damage, gives back True if this hit killed it'''
        if not self.alive:
            return False
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            return True
        return False

    def update(self, dt):
        '''what the enemy does each step, the basic one just stands there'''

    def draw(self, surface, theme):
        if not self.alive:
            return
        centre = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, self.color, centre, int(self.radius))
        pygame.draw.circle(surface, theme.panel_border, centre,
                           int(self.radius), 2)
        if self.hp < self.max_hp:
            # little hp bar above the head, every subclass gets it from here
            bar_w = 40
            x = int(self.position.x - bar_w / 2)
            y = int(self.position.y - self.radius - 12)
            pygame.draw.rect(surface, (40, 40, 40), (x, y, bar_w, 5))
            filled = int(bar_w * self.hp / self.max_hp)
            pygame.draw.rect(surface, theme.good, (x, y, filled, 5))


class Rockling(Enemy):
    '''the basic enemy, just stands there, dies to one good hit'''

    def __init__(self, position):
        super().__init__("rockling", position, max_hp=15, points=100,
                         radius=16.0, color=(210, 120, 90))


class ArmouredRockling(Enemy):
    '''bigger tougher rockling, takes a few hits to break'''

    def __init__(self, position):
        super().__init__("armoured_rockling", position, max_hp=50,
                         points=250, radius=24.0, color=(120, 120, 160))


class Skitterer(Enemy):
    '''level 3 enemy, walks between two x positions so the player
    has to lead the shot'''

    def __init__(self, position, patrol=(0, 0), speed=90.0):
        super().__init__("Skitterer", position, max_hp=25, points=150,
                         radius=15.0, color=(190, 200, 90))
        self.x_min = min(patrol)
        self.x_max = max(patrol)
        self.speed = speed
        self.direction = 1

    def update(self, dt):
        '''walks back and forth between x_min and x_max'''
        if not self.alive:
            return
        self.position.x += self.direction * self.speed * dt
        if self.position.x <= self.x_min:
            self.position.x = self.x_min
            self.direction = 1
        elif self.position.x >= self.x_max:
            self.position.x = self.x_max
            self.direction = -1


class ColossusBoss(Enemy):
    '''level 4 boss, big and tough so it takes a few hits'''

    def __init__(self, position):
        super().__init__("Colossus Boss", position,
                         max_hp=settings.Boss_max_hp, points=1000,
                         radius=44.0, color=(150, 70, 170))
        self.shields_remaining = 3

    def take_damage(self, amount):
        if self.phase == 2:
            # weak point is open so hits do double damage
            amount = amount * settings.Boss_weak_point_multiplier
        return super().take_damage(amount)

    @property
    def phase(self):
        '''worked out from the shields and hp each time so it
        cant get out of date'''
        if self.shields_remaining > 0:
            return 1
        if self.hp > self.max_hp * settings.Boss_enrage_hp_fraction:
            return 2
        return 3

    @property
    def enraged(self):
        return self.phase == 3

    def draw(self, surface, theme):
        super().draw(surface, theme)
        if not self.alive:
            return
        # big hp bar with the phase number on it
        bar_w = 180
        x = int(self.position.x - bar_w / 2)
        y = int(self.position.y - self.radius - 18)
        pygame.draw.rect(surface, (30, 30, 30), (x, y, bar_w, 10))
        filled = int(bar_w * self.hp / self.max_hp)
        color = theme.good if self.phase < 3 else theme.danger
        pygame.draw.rect(surface, color, (x, y, filled, 10))
        font = get_font(14)
        label = font.render(f"Phase {self.phase}", True, theme.text)
        surface.blit(label, (x, y - 18))


'''the enemy types a level spec can ask for, keyed by the name used in
the level files'''
ENEMY_TYPES = {
    "rockling": Rockling,
    "armored_brute": ArmouredRockling,
    "skitterer": Skitterer,
    "colossus_boss": ColossusBoss,
}
