
from skyhurler.maingame.levels.level1 import Level1
from skyhurler.maingame.levels.Level2 import Level2
from skyhurler.maingame.levels.level3 import Level3
from skyhurler.maingame.levels.Level4 import Level4

'''works out which level class to use for a level number'''
def make_level(level_number):
    if level_number == 1:
        return Level1()
    if level_number == 2:
        return Level2()
    if level_number == 3:
        return Level3()
    if level_number == 4:
        return Level4()
    # shouldnt ever happen, just in case
    return Level1()
