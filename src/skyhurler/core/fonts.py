'''gives back a font for the size asked and keeps it in a cache so a new
one isnt made every frame'''

from functools import lru_cache

import pygame









def get_font(size, bold=False):
    return pygame.font.SysFont("arial", size, bold=bold)
