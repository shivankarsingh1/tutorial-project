from skyhurler.core.Scene import Scene
from skyhurler.ui.widgets import Label, Button

class MinigameSkyDice(Scene):

    def enter(self):
        def go_back():
            self.context.scenes.switch("main_menu")
        '''all widgets in one place'''
        self.widgets = [
            Label((0 , 40 , 1280 , 70), 'SkyDice', font_size = 64),            
            Button((540, 400, 200, 56), 'Back to Menu', go_back),

        ]

    '''stops checkng for events if a button is clicked'''
    def handle_event(self, event):
        for widget in self.widgets:
            if widget.handle_event(event):
                return

    def update(self, dt):
        for widget in self.widgets:
            widget.update(dt)

    '''fils background whith black'''
    def draw(self, surface):
        surface.fill((0, 0, 0))

        for widget in self.widgets:
            widget.draw(surface, self.context.themes.current_theme)

            