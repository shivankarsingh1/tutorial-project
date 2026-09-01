

from pygame.math import Vector2

''' A hit is a colliion between two objects '''
class Hit:

    def __init__(self, struck, normal, penetration, impact_velocity,
                 restitution=0.3, friction=0.1):
        self.struck = struck
        self.normal = normal
        self.penetration = penetration
        self.impact_velocity = impact_velocity
        self.restitution = restitution
        self.friction = friction


''' Collision detection functions. Each returns a Hit object if a collision'''
def circle_circle(position, radius, other_position, other_radius, struck,
                  impact_velocity, restitution=0.3, friction=0.1):
    offset = Vector2(position) - Vector2(other_position)
    distance = offset.length()
    overlap = radius + other_radius - distance
    if overlap <= 0:
        return None
    if distance == 0:
        normal = Vector2(0, -1)
    else:
        normal = offset / distance
    return Hit(struck, normal, overlap, Vector2(impact_velocity),
               restitution, friction)


def circle_rect(position, radius, rect, struck, impact_velocity,
                restitution=0.3, friction=0.1):
    centre = Vector2(position)
    closest = Vector2(
        max(rect.left, min(centre.x, rect.right)),
        max(rect.top, min(centre.y, rect.bottom)),
    )
    offset = centre - closest
    distance = offset.length()
    if distance >= radius:
        return None
    if distance > 0:
        normal = offset / distance
        penetration = radius - distance
    else:
        left = centre.x - rect.left
        right = rect.right - centre.x
        top = centre.y - rect.top
        bottom = rect.bottom - centre.y
        smallest = min(left, right, top, bottom)
        if smallest == left:
            normal, penetration = Vector2(-1, 0), radius + left
        elif smallest == right:
            normal, penetration = Vector2(1, 0), radius + right
        elif smallest == top:
            normal, penetration = Vector2(0, -1), radius + top
        else:
            normal, penetration = Vector2(0, 1), radius + bottom
    return Hit(struck, normal, penetration, Vector2(impact_velocity),
               restitution, friction)


def circle_rect_overlap(position, radius, rect):
    centre = Vector2(position)
    closest = Vector2(
        max(rect.left, min(centre.x, rect.right)),
        max(rect.top, min(centre.y, rect.bottom)),
    )
    return centre.distance_to(closest) <= radius
