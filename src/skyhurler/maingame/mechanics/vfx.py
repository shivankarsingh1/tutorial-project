from skyhurler.physics.rigidbody import Rigidbody

import random
from pygame.math import Vector2

class Particle(Rigidbody):

    def __init__(self, position, color, speed, lifetime):
        super().__init__(mass=1.0, position=position, radius=3.0,
                         restitution=0.0, lifetime=lifetime)
        angle = random.uniform(0, 360)
        self.velocity = Vector2(1, 0).rotate(angle) * speed
        self.color = color

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.engine = None

    def bind(self, engine):
        self.engine = engine

    def burst(self, position, color, count=14, speed=220.0, lifetime=0.8):
        for _ in range(count):
            jitter = Vector2(random.uniform(-8, 8), random.uniform(-8, 8))
            particle = Particle(Vector2(position) + jitter, color,
                                speed * random.uniform(0.4, 1.0),
                                lifetime * random.uniform(0.6, 1.2))
            self.particles.append(particle)
            if self.engine is not None:
                self.engine.add_body(particle)

    def prune(self):
        self.particles = [p for p in self.particles
                          if p.age < (p.lifetime or 0)]

    def draw(self, surface):
        for particle in self.particles:
            if particle.age >= (particle.lifetime or 0):
                continue
            x, y = int(particle.position.x), int(particle.position.y)
            surface.fill(particle.color, (x, y, 3, 3))
