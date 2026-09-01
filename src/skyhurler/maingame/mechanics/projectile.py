import math

import pygame
from pygame.math import Vector2

from skyhurler.core import settings
from skyhurler.maingame.mechanics import materials
from skyhurler.maingame.mechanics.collision import circle_circle, circle_rect
from skyhurler.physics.rigidbody import Rigidbody


class Projectile(Rigidbody):
    def __init__(self, character, position, sprite=None):
        mass = character.mass
        radius = 20.0 * character.size
        super().__init__(mass=mass, position=position, radius=radius)
        self.character = character
        self.sprite = sprite
        self._scaled_size = None
        self._scaled_surface = None
        self.launch_angle = 0.0
        self.launch_power = 0.0
        self.has_collided = False

    def launch(self, drag_vector):
        drag = Vector2(drag_vector)
        if drag.length() > settings.Drag_radius:
            drag.scale_to_length(settings.Drag_radius)

        velocity = drag * -settings.Power_scale
        if velocity.length() > settings.Max_launch_power:
            velocity.scale_to_length(settings.Max_launch_power)
        velocity = velocity * self.character.launch_power

        self.velocity.update(velocity)
        self.launch_power = velocity.length()
        self.launch_angle = math.degrees(math.atan2(-velocity.y, velocity.x))

    @property
    def is_splitter(self):
        return self.character.name == "Splitter"

    def check_collision(self, enemies, obstacles, ground_rect):
        hits = []
        for enemy in enemies:
            # if not enemy.alive:
            #     continue
            hit = circle_circle(
                self.position, self.radius,
                enemy.position, enemy.radius,
                struck=enemy,
                impact_velocity=self.velocity,
                restitution=0.4, friction=0.1,
            )
            if hit:
                hits.append(hit)
        for obstacle in obstacles:
            if obstacle.destroyed:
                continue
            hit = circle_rect(
                self.position, self.radius, obstacle.rect,
                struck=obstacle,
                impact_velocity=self.velocity,
                restitution=obstacle.restitution,
                friction=obstacle.friction,
            )
            if hit:
                hits.append(hit)
        if ground_rect is not None:
            hit = circle_rect(
                self.position, self.radius, ground_rect,
                struck=ground_rect,
                impact_velocity=self.velocity,
                restitution=materials.Terrain.restitution,
                friction=materials.Terrain.friction,
            )
            if hit:
                hits.append(hit)
        if hits:
            self.has_collided = True
        return hits

    def register_with(self, engine, enemies, obstacles, ground_rect):
        engine.add_body(self)

        def check():
            return self.check_collision(enemies, obstacles, ground_rect)

        engine.set_narrow_phase(self, check)


    def scaled_sprite(self):
        size = max(2, int(self.radius * 2))
        if self._scaled_surface is None or self._scaled_size != size:
            self._scaled_surface = pygame.transform.scale(
                self.sprite, (size, size))
            self._scaled_size = size
        return self._scaled_surface

    def draw(self, surface, theme):
        centre = (int(self.position.x), int(self.position.y))
        if self.sprite is None:
            pygame.draw.circle(surface, self.character.color, centre,
                               int(self.radius))
            pygame.draw.circle(surface, theme.text, centre, int(self.radius), 2)
            return
        image = self.scaled_sprite()
        if self.velocity.length() > 1.0:
            angle = math.degrees(math.atan2(-self.velocity.y,
                                            self.velocity.x))
            image = pygame.transform.rotate(image, angle)
        surface.blit(image, image.get_rect(center=centre))
