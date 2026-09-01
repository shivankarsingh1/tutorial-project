
import pygame

from skyhurler.core.Scene import Scene
from skyhurler.ui.widgets import Button, Label

''' overlay scene for pausing the game'''
class PauseOverlay(Scene):
    def enter(self):
        context = self.context
        scenes = context.scenes

        def resume():
            context.audio.play_sfx("ui_click")
            scenes.pop()

        def retry():
            context.audio.play_sfx("ui_click")
            ''' restart the level that was being played when pause was pressed'''
            scenes.switch(f"level{context.current_level}")

        def to_menu():
            context.audio.play_sfx("ui_click")
            scenes.switch("main_menu")

        ''' all widgets stored in one list'''
        self.widgets = [
            Label((0, 200, 1280, 60), "Paused", font_size=54),
            Button((540, 300, 200, 50), "Resume", resume),
            Button((540, 366, 200, 50), "Retry", retry),
            Button((540, 432, 200, 50), "Menu", to_menu),
        ]

    ''' handle events for the scene'''
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            ''' resume the game if escape is pressed again'''
            self.context.scenes.pop()
            return
        for widget in self.widgets:
            if widget.handle_event(event):
                return

    ''' update the scene'''
    def update(self, dt):
        pass   


    ''' draw the scene'''
    def draw(self, surface):
        theme = self.context.themes.current_theme
        ''' fill the background with a dimmed overlay'''
        dim = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        dim.fill((8, 10, 16, 110))
        surface.blit(dim, (0, 0))
        for widget in self.widgets:
            widget.draw(surface, theme)

            
