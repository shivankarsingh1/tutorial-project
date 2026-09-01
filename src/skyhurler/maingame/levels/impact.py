import pygame

from skyhurler.core import settings
from skyhurler.core.cascade import (bomb_chain, collapse_zone,
                                    enemy_in_collapse_zone, run_cascade)
from skyhurler.maingame.characters.enemy import ColossusBoss, Enemy
from skyhurler.maingame.mechanics.collision import circle_rect_overlap
from skyhurler.maingame.mechanics.obstacle import Obstacle
from skyhurler.maingame.mechanics.projectile import Projectile

'''Class to take impact in gane'''
class ImpactResolver:

    def __init__(self, scene):
        self.scene = scene

    def on_hit(self, body, hit):
        scene = self.scene
        if scene.finished or not isinstance(body, Projectile):
            return
        speed = hit.impact_velocity.length()
        if speed < 40:
            return
        struck = hit.struck

        if isinstance(struck, pygame.Rect):
            if speed > 150:
                scene.context.audio.play_sfx("impact")
                scene.vfx.burst(body.position, (150, 140, 120), 6,
                                speed=90.0, lifetime=0.4)
            return

        damage = settings.Impact_damage_scale * body.mass * speed

        if isinstance(struck, Enemy):
            killed = struck.take_damage(damage)
            if killed:
                self._kill_enemy(struck)
            else:
                scene.context.audio.play_sfx("impact")
            return

        if isinstance(struck, Obstacle):
            destroyed = struck.take_damage(damage)
            if destroyed:
                self._on_obstacle_destroyed(struck)
            elif speed > 150:
                scene.context.audio.play_sfx("impact")

    def _on_obstacle_destroyed(self, obstacle, allow_cascade=True):
        scene = self.scene
        scene.tracker.add_obstacle_points(obstacle)
        scene.vfx.burst(obstacle.center, obstacle.material.color, 16)
        scene.context.audio.play_sfx("destruction")

        if obstacle.material.name == "bomb shell":
            self._explode(obstacle)
            return
        if obstacle.role == "shield":
            boss = scene.level.boss()
            if boss is not None:
                boss.shields_remaining = max(0, boss.shields_remaining - 1)

        if allow_cascade:
            broken_extra = self._apply_cascade(obstacle)
            for target in broken_extra:
                self._on_obstacle_destroyed(target, allow_cascade=False)

    def _apply_cascade(self, obstacle):
        scene = self.scene
        obstacles = scene.level.obstacles
        index = obstacles.index(obstacle)
        base = obstacle.material.strength / settings.Cascade_falloff
        spread = run_cascade(index, obstacles,
                             scene.level.defn.chain_links,
                             scene.level.defn.supports, base)
        broken = []
        for i, damage in spread:
            target = obstacles[i]
            if target.destroyed:
                continue
            if target.take_damage(damage):
                broken.append(target)
        if broken:
            zone = collapse_zone([obstacle] + broken)
            for enemy in scene.level.enemies:
                if enemy.alive and enemy_in_collapse_zone(enemy, zone):
                    enemy.take_damage(settings.Collapse_enemy_damage)
        return broken

    def _kill_enemy(self, enemy):
        scene = self.scene
        scene.tracker.add_enemy_points(enemy)
        scene.vfx.burst(enemy.position, enemy.color, 20)
        scene.context.audio.play_sfx("destruction")
        if enemy.platform is not None and not enemy.platform.destroyed:
            enemy.platform.destroyed = True
            self._on_obstacle_destroyed(enemy.platform)
        if isinstance(enemy, ColossusBoss):
            scene.vfx.burst(enemy.position, enemy.color, 30,
                            speed=340.0, lifetime=1.2)

    def _explode(self, bomb):
        scene = self.scene
        scene.context.audio.play_sfx("explosion")
        scene.vfx.burst(bomb.center, (250, 170, 60), 34, speed=340.0,
                        lifetime=0.9)
        detonating = bomb_chain(scene.level.obstacles, bomb,
                                bomb.blast_radius)
        for other in detonating:
            other.destroyed = True
            scene.tracker.add_obstacle_points(other)
            scene.vfx.burst(other.center, (250, 170, 60), 34, speed=340.0,
                            lifetime=0.9)
        for source in detonating:
            centre = source.center
            radius = source.blast_radius
            for enemy in scene.level.enemies:
                if not enemy.alive:
                    continue
                distance = centre.distance_to(enemy.position)
                if distance <= radius:
                    falloff = 1.0 - 0.5 * (distance / radius)
                    if enemy.take_damage(source.blast_damage * falloff):
                        self._kill_enemy(enemy)
            for obstacle in scene.level.obstacles:
                if obstacle.destroyed or obstacle is source:
                    continue
                if circle_rect_overlap(centre, radius, obstacle.rect):
                    if obstacle.take_damage(source.blast_damage):
                        self._on_obstacle_destroyed(obstacle)
            for body in list(scene.engine.bodies):
                if body.is_kinematic or body.lifetime is not None:
                    continue
                offset = body.position - centre
                distance = offset.length()
                if 0 < distance <= radius:
                    direction = offset / distance
                    strength = source.blast_impulse * (1.0 - distance / radius)
                    body.apply_impulse(direction * strength * body.mass)
