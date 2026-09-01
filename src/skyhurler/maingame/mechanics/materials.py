class Material:
    '''the physical stats of one buildable material'''

    def __init__(self, name, strength, restitution, friction, points, color):
        self.name = name
        self.strength = strength
        self.restitution = restitution
        self.friction = friction
        self.points = points
        self.color = color


Wood = Material("wood", 25, 0.25, 0.15, 10, (150, 105, 60))
Stone = Material("stone", 70, 0.10, 0.30, 15, (130, 132, 138))
Glass = Material("glass", 10, 0.05, 0.05, 20, (170, 220, 235))
Elastic = Material("elastic", 200, 0.95, 0.05, 5, (240, 130, 200))
Terrain = Material("terrain", 55, 0.30, 0.40, 5, (100, 140, 90))
Bomb_shell = Material("bomb shell", 12, 0.20, 0.20, 25, (200, 80, 60))

'''every material a level can be built out of, looked up by name'''
MATERIALS = {
    "wood": Wood,
    "stone": Stone,
    "glass": Glass,
    "elastic": Elastic,
    "terrain": Terrain,
    "bomb shell": Bomb_shell,
}
