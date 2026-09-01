import pygame

from skyhurler.core.Scene import Scene
from skyhurler.core.fonts import get_font
from skyhurler.ui.widgets import Button


class LevelSelect(Scene):

    def choose_back(self):
        self.context.audio.play_sfx("ui_click")
        self.context.scenes.switch("main_menu")

    '''each level button stores its number on the context, then opens
    character select first'''
    def choose_level_1(self):
        self.context.audio.play_sfx("ui_click")
        self.context.current_level = 1
        self.context.scenes.push("character_select")

    def choose_level_2(self):
        self.context.audio.play_sfx("ui_click")
        self.context.current_level = 2
        self.context.scenes.push("character_select")

    def choose_level_3(self):
        self.context.audio.play_sfx("ui_click")
        self.context.current_level = 3
        self.context.scenes.push("character_select")

    def choose_level_4(self):
        self.context.audio.play_sfx("ui_click")
        self.context.current_level = 4
        self.context.scenes.push("character_select")

    def enter(self):
        '''all widgets stored in one list; rebuilt on enter so the lock
        states refresh after a level is beaten'''
        self.title_surf = get_font(56, bold=True).render(
            "SELECT LEVEL", True, (255, 255, 255))
        progress = self.context.progress
        self.widgets = [
            Button((443, 240, 180, 56), "Level 1", self.choose_level_1,
                   font_size=22, enabled=progress.is_level_unlocked(1)),
            Button((663, 240, 180, 56), "Level 2", self.choose_level_2,
                   font_size=22, enabled=progress.is_level_unlocked(2)),
            Button((443, 316, 180, 56), "Level 3", self.choose_level_3,
                   font_size=22, enabled=progress.is_level_unlocked(3)),
            Button((663, 316, 180, 56), "Level 4", self.choose_level_4,
                   font_size=22, enabled=progress.is_level_unlocked(4)),
            Button((540, 413, 200, 50), "Back to Menu",
                   self.choose_back, font_size=22),
        ]

    '''stops checking for events if a button is clicked'''
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.context.scenes.switch("main_menu")
            return
        for widget in self.widgets:
            if widget.handle_event(event):
                return

    def update(self, dt):
        pass

    def draw(self, surface):
        '''background drawn black'''
        surface.fill((0, 0, 0))
        surface.blit(self.title_surf, (30, 55))
        theme = self.context.themes.current_theme
        for widget in self.widgets:
            widget.draw(surface, theme)
