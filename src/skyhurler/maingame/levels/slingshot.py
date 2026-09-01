from pygame.math import Vector2

GRAB_DISTANCE = 80
MIN_DRAG = 10


class Slingshot:

    def __init__(self, level):
        self.level = level
        self.dragging = False
        self.drag_pos = Vector2(0, 0)
        self.loaded = None

    def grab(self, pos, character, sprite=None):
        if self.loaded is not None or self.level.projectiles_remaining <= 0:
            return False
        anchor = Vector2(self.level.defn.launch_pos)
        if Vector2(pos).distance_to(anchor) >= GRAB_DISTANCE:
            return False
        self.loaded = self.level.take_projectile(character, sprite)
        if self.loaded is None:
            return False
        self.dragging = True
        self.drag_pos.update(pos)
        return True

    def release(self):
        self.dragging = False
        drag = Vector2(self.level.defn.launch_pos) - self.drag_pos
        if drag.length() < MIN_DRAG:
            self.cancel()
            return None
        return drag

    def cancel(self):
        self.dragging = False
        if self.loaded is not None:
            self.level.live_projectiles.remove(self.loaded)
            self.level.projectiles_remaining += 1
            self.loaded = None
