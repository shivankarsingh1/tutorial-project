

from pygame.math import Vector2

from skyhurler.core import settings

''' A rigidbody is a physical object that can move and collide with other objects. It has a position, velocity, mass, and radius. It can be kinematic (not affected by forces) or dynamic (affected by forces). It can have a restitution (bounciness) and a lifetime (how long it exists). It can be at rest or moving. It can have a contact with another object. It can have a force applied to it. It can have an age (how long it has existed). It can have a force expired (if it has been at rest for too long).'''
class Rigidbody:
    def __init__(self, mass=1.0, position=(0.0, 0.0), radius=10.0,
                 is_kinematic=False, restitution=None, lifetime=None):
        self.mass = max(0.0001, mass)  # never zero, we divide by it
        self.position = Vector2(position)
        self.velocity = Vector2(0.0, 0.0)
        self.radius = radius

        self.is_kinematic = is_kinematic

        self.restitution = restitution

        self.lifetime = lifetime


        self.force = Vector2(0.0, 0.0)

        self.is_moving = True
        self.contact = False
        self.rest_steps = 0
        self.age = 0.0
        self.force_expired = False

    def apply_gravity(self, gravity):

        self.force += Vector2(gravity) * self.mass

    def apply_force(self, force):
        self.force += Vector2(force)
        self._wake()

    def apply_impulse(self, impulse):
        self.velocity += Vector2(impulse) / self.mass
        self._wake()

    def _wake(self):
        self.is_moving = True
        self.rest_steps = 0
        self.force_expired = False

    def update(self, dt):

        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.force = Vector2(0.0, 0.0)
        self.age += dt

    @property
    def speed(self):
        return self.velocity.length()

    def at_rest(self):
        return self.force_expired or not self.is_moving

    def check_rest_rule(self):

        return self.speed < settings.Rest_speed and self.contact
