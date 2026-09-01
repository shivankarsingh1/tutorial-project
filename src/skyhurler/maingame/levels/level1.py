from skyhurler.maingame.levels.base_level import BaseLevel, LevelDef

'''LEVEL 1 of the game'''
class Level1(BaseLevel):
    index = 1

    def __init__(self):
        super().__init__(LevelDef(
            name="First Flight",
            description="Learn the sling. Three Rocklings, one good hit each.",
            enemies=[
                {"type": "rockling", "pos": (900, 640)},
                {"type": "rockling", "pos": (1010, 640)},
                {"type": "rockling", "pos": (955, 600), "stand_on": 2},
            ],
            obstacles=[
                {"rect": (860, 616, 24, 48), "material": "wood"},
                {"rect": (1020, 616, 24, 48), "material": "wood"},
                {"rect": (935, 616, 40, 44), "material": "wood"},
            ],
            projectiles=5,
            launch_pos=(150, 570),
        ))

