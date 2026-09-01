
from collections import deque

from skyhurler.core import settings
from skyhurler.maingame.mechanics.collision import circle_rect_overlap

''' cascade of destruction starting from a broken index'''
def run_cascade(broken_index, obstacles, chain_links, supports, base_damage):

    neighbours = {}
    for a, b in chain_links:
        neighbours.setdefault(a, []).append(b)
        neighbours.setdefault(b, []).append(a)
    for a, b in supports:

        neighbours.setdefault(a, []).append(b)

    results = []
    visited = {broken_index}
    queue = deque([(broken_index, 0)])

    while queue:
        index, depth = queue.popleft()
        if depth >= settings.Max_cascade_depth:
            continue
        for neighbour in neighbours.get(index, []):
            if neighbour in visited:
                continue
            visited.add(neighbour)
            damage = base_damage * (settings.Cascade_falloff ** (depth + 1))
            results.append((neighbour, damage))
            queue.append((neighbour, depth + 1))
    return results


def collapse_zone(destroyed_obstacles):

    rects = []
    for obstacle in destroyed_obstacles:
        rect = obstacle.rect.copy()
        rect.inflate_ip(int(settings.Collapse_margin * 2),
                        int(settings.Collapse_margin * 2))
        rects.append(rect)
    return rects


def enemy_in_collapse_zone(enemy, zone_rects):

    return any(circle_rect_overlap(enemy.position, enemy.radius, rect)
               for rect in zone_rects)


def bomb_chain(bombs, first_bomb, blast_radius, max_depth=None):

    if max_depth is None:
        max_depth = settings.Max_cascade_depth
    order = [first_bomb]
    visited = {id(first_bomb)}
    queue = deque([(first_bomb, 0)])

    while queue:
        bomb, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for other in bombs:
            if other is bomb or other.destroyed or id(other) in visited:
                continue
            if bomb.center.distance_to(other.center) <= blast_radius:
                visited.add(id(other))
                order.append(other)
                queue.append((other, depth + 1))
    return order
