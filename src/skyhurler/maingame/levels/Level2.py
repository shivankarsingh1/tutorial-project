from skyhurler.maingame.levels.base_level import BaseLevel, LevelDef

'''LEVEL 2 of'''
class Level2(BaseLevel):
    index = 2

    def __init__(self):
        super().__init__(LevelDef(
            name="Stone Wall",
            description="A stone wall guards the pack. Lob over it or smash through.",
            enemies=[
                {"type": "rockling", "pos": (980, 640)},
                {"type": "rockling", "pos": (1050, 640)},
                {"type": "rockling", "pos": (1120, 640)},
                {"type": "rockling", "pos": (1190, 640)},
            ],
            obstacles=[
                {"rect": (900, 568, 26, 96), "material": "stone"},
                {"rect": (1010, 616, 24, 48), "material": "wood"},
                {"rect": (1160, 616, 24, 48), "material": "wood"},
            ],
            projectiles=5,
            launch_pos=(150, 570),
        ))