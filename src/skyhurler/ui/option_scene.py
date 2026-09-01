from skyhurler.ui.widgets import Button, Label
from skyhurler.core.Scene import Scene

class OptionScene(Scene):

    def __init__(self, context):
        super().__init__(context)
        self.music_on = not context.audio.muted
        self.music_button = None

    def music_toggle(self):
         '''un/mutes through the AudioManager so the volume and the saved
         setting stay in sync with what the button shows'''
         self.music_on = not self.context.audio.toggle_mute()
         if self.music_button:
            self.music_button.text = 'Music: On' if self.music_on else 'Music: Off'

    def enter(self):
        def go_back():
            self.context.scenes.switch("main_menu")
        
        '''all widgets in one place'''
        self.music_button = Button((440, 220, 400, 56), 'Music: On' if self.music_on else 'Music: Off', self.music_toggle)
        self.widgets = [
            Label((0 , 40 , 1280 , 70), 'Options', font_size = 64),
            Button((540, 160, 80, 40), "+", go_back),
            Button((660, 160, 80, 40), "-", go_back),
            self.music_button,
            Button((440, 300, 400, 56), 'Fullscreen', go_back),
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

    '''fills background with the current theme sky colour'''
    def draw(self, surface):
        theme = self.context.themes.current_theme
        surface.fill(theme.sky)

        for widget in self.widgets:
            widget.draw(surface, theme)











            


