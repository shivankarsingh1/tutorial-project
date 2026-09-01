import pygame

from skyhurler.core.Scene import Scene
from skyhurler.ui.widgets import Button


class MainMenu(Scene):
    '''the main menu screen'''

    def enter(self):
        scenes = self.context.scenes

        def quit_game():
            self.context.quit_requested = True

        # one row per button (label, what it does, y position)
        rows = [
            ("Skyhurler  (main game)", lambda: scenes.switch("level_select"), 197),
            ("SkyDice (mini game 1)", lambda: scenes.switch("minigame_skydice"), 275),
            ("SkyRunner (mini game 2)", lambda: scenes.switch("minigame_skyrunner"), 353),
            ("Option", lambda: scenes.switch("options"), 431),
            ("Quit", quit_game, 509),
        ]
        self.buttons = [Button((0, y, 300, 56), text, on_click)
                        for text, on_click, y in rows]

        white = (235, 238, 245)
        dim = (140, 150, 170)
        # title made once so we dont render it every frame
        self.title_surf = pygame.font.Font(None, 64).render("SKYHURLER", True, white)
        self.sub_surf = pygame.font.Font(None, 20).render("Shivora Games", True, dim)

    def handle_event(self, event):
        '''escape quits the game, otherwise the buttons get the event'''
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.context.quit_requested = True
            return
        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self, dt):
        pass

    def draw(self, surface):
        '''buttons drawn in the middle of the screen'''
        theme = self.context.themes.current_theme
        surface.fill((0, 0, 0))
        w = surface.get_width()

        surface.blit(self.title_surf, (w // 2 - self.title_surf.get_width() // 2, 75))
        surface.blit(self.sub_surf, (w // 2 - self.sub_surf.get_width() // 2, 140))

        for button in self.buttons:
            button.rect.centerx = w // 2
            button.draw(surface, theme)
