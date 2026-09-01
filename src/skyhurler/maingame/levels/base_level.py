import pygame

from skyhurler.core import settings
from skyhurler.maingame.characters.enemy import (ENEMY_TYPES, ColossusBoss,
                                                 Skitterer)
from skyhurler.maingame.mechanics.bomb import Bomb
from skyhurler.maingame.mechanics.materials import MATERIALS
from skyhurler.maingame.mechanics.obstacle import Obstacle
from skyhurler.maingame.mechanics.projectile import Projectile

'''holds all the data one level is built out of'''
class LevelDef:

    def __init__(self, name, description, enemies, obstacles, projectiles,
                 launch_pos, chain_links=None, supports=None, wind=None,
                 friction_zones=None):
        self.name = name
        self.description = description
        self.enemies = enemies
        self.obstacles = obstacles
        self.projectiles = projectiles
        self.launch_pos = launch_pos
        self.wind = wind
        if chain_links is None:
            chain_links = []
        self.chain_links = chain_links
        if supports is None:
            supports = []
        self.supports = supports
        if friction_zones is None:
            friction_zones = []
        self.friction_zones = friction_zones


class BaseLevel:
    index = 0

    def __init__(self, level_def=None):
        if level_def is None:
            '''no layout written yet - a blank sandbox level'''
            level_def = LevelDef(name=f"Level {self.index}", description="",
                                 enemies=[], obstacles=[], projectiles=0,
                                 launch_pos=(150, 570))
        self.defn = level_def
        self.load()

    def load(self):
        '''(re)builds everything in the level from its defn'''
        d = self.defn
        self.obstacles = []
        for spec in d.obstacles:
            self.obstacles.append(self._spawn_obstacle(spec))
        self.enemies = []
        for spec in d.enemies:
            self.enemies.append(self._spawn_enemy(spec))
        self.projectiles_remaining = d.projectiles
        self.live_projectiles = []
        self.ground_rect = pygame.Rect(0, settings.Ground_top,
                                       settings.World_width,
                                       settings.World_height - settings.Ground_top)

    def _spawn_enemy(self, spec):
        '''makes one enemy from a spec dict in the level defn'''
        kind = spec["type"]
        pos = spec["pos"]
        if kind == "skitterer":
            # skitterers can be given a patrol area and speed in the spec
            enemy = Skitterer(pos, patrol=spec.get("patrol", (0, 0)),
                              speed=spec.get("speed", 90.0))
        elif kind == "colossus_boss":
            enemy = ColossusBoss(pos)
        else:
            # rocklings and armoured ones only need a position
            enemy = ENEMY_TYPES[kind](pos)
        if "stand_on" in spec:
            enemy.platform = self.obstacles[spec["stand_on"]]
        return enemy

    def _spawn_obstacle(self, spec):
        rect = spec["rect"]
        material_name = spec["material"]
        if material_name == "bomb shell":
            obstacle = Bomb(rect)
        else:
            obstacle = Obstacle(rect, MATERIALS[material_name])
        obstacle.role = spec.get("role")
        return obstacle

    def reset(self):
        self.load()

    def boss(self):
        for enemy in self.enemies:
            if isinstance(enemy, ColossusBoss):
                return enemy
        return None

    def enemies_remaining(self):
        return sum(1 for e in self.enemies if e.alive)

    def is_complete(self):
        return bool(self.defn.enemies) and self.enemies_remaining() == 0

    def has_failed(self):
        if not self.defn.enemies:
            return False
        if self.projectiles_remaining > 0:
            return False
        if self.is_complete():
            return False
        return all(p.at_rest() for p in self.live_projectiles)

    def take_projectile(self, character, sprite=None):
        if self.projectiles_remaining <= 0:
            return None
        self.projectiles_remaining -= 1
        projectile = Projectile(character, self.defn.launch_pos, sprite)
        self.live_projectiles.append(projectile)
        return projectile

    def clear_settled_projectiles(self):
        settled = [p for p in self.live_projectiles if p.at_rest()]
        self.live_projectiles = [p for p in self.live_projectiles
                                 if not p.at_rest()]
        return settled







