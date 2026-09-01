

from math import ceil

from pygame.math import Vector2

from skyhurler.core import settings


class PhysicsEngine:
    def __init__(self):
        self.gravity = Vector2(settings.Gravity)
        self.bounds = settings.World_size

        self.bodies = []
        self.fields = []
        self.drags = []
        self._checks = {}
        self._responders = []

    def add_body(self, body):
        if body not in self.bodies:
            self.bodies.append(body)
        return body

    def remove_body(self, body):
        if body in self.bodies:
            self.bodies.remove(body)
        self._checks.pop(body, None)

    def set_narrow_phase(self, body, check):
        self._checks[body] = check

    def add_responder(self, responder):
        self._responders.append(responder)

    def add_field(self, rect, accel):
        self.fields.append((rect, Vector2(accel)))
        return rect, Vector2(accel)

    def add_drag(self, rect, coefficient):
        self.drags.append((rect, coefficient))
        return rect, coefficient

    def step(self, dt):
        for body in list(self.bodies):
            if body.lifetime is not None and body.age >= body.lifetime:
                self.remove_body(body)
        for body in list(self.bodies):
            self._step_body(body, dt)

    def _step_body(self, body, dt):
        if body.is_kinematic or body.at_rest():
            return

        travel = body.velocity.length() * dt
        if body.radius > 0 and travel > body.radius:
            substeps = min(settings.Max_substeps, ceil(travel / body.radius))
        else:
            substeps = 1
        sub_dt = dt / substeps

        for _ in range(substeps):
            was_in_contact = body.contact
            body.contact = False

            if not was_in_contact:
                for rect, accel in self.fields:
                    if rect.collidepoint(body.position):
                        body.apply_force(accel * body.mass)

            body.apply_gravity(self.gravity)
            body.update(sub_dt)

            for rect, coefficient in self.drags:
                if rect.collidepoint(body.position):
                    body.velocity *= max(0.0, 1.0 - coefficient * sub_dt)

            check = self._checks.get(body)
            if check is not None:
                for hit in check():
                    self._resolve(body, hit)
            self._clamp_to_bounds(body)

        self._update_rest(body)

    def _resolve(self, body, hit):
        body.contact = True
        body.position += hit.normal * hit.penetration

        restitution = (body.restitution if body.restitution is not None
                       else hit.restitution)

        into_surface = body.velocity.dot(hit.normal)
        if into_surface < 0:
            body.velocity -= hit.normal * into_surface * (1.0 + restitution)

        along_normal = body.velocity.dot(hit.normal)
        tangential = body.velocity - hit.normal * along_normal
        body.velocity = hit.normal * along_normal + tangential * (1.0 - hit.friction)

        for responder in self._responders:
            responder(body, hit)

    def _clamp_to_bounds(self, body):
        w, h = self.bounds
        r = body.radius
        if body.position.x < r:
            body.position.x = r
            body.velocity.x = max(0.0, body.velocity.x)
            body.contact = True
        elif body.position.x > w - r:
            body.position.x = w - r
            body.velocity.x = min(0.0, body.velocity.x)
            body.contact = True
        if body.position.y < r:
            body.position.y = r
            body.velocity.y = max(0.0, body.velocity.y)
            body.contact = True
        elif body.position.y > h - r:
            body.position.y = h - r
            body.velocity.y = min(0.0, body.velocity.y)
            body.contact = True

    def _update_rest(self, body):
        if body.lifetime is not None or body.is_kinematic:
            return
        if body.age >= settings.Max_shot_time:
            body.force_expired = True
        if body.force_expired or body.check_rest_rule():
            body.rest_steps += 1
        else:
            body.rest_steps = 0
        if body.rest_steps >= settings.Rest_steps or body.force_expired:
            body.is_moving = False
            body.velocity = Vector2(0.0, 0.0)
        else:
            body.is_moving = True
