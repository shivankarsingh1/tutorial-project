from skyhurler.core.Scene import Scene
from skyhurler.ui.widgets import Button, Label


class CompletionScene(Scene):

    def enter(self):
        self.widgets = [
            Label((0, 40, 1280, 70), 'Level complete, WELL DONE!',
                  font_size=64),
            Button((540, 400, 200, 56), 'Back to Level Select',
                   lambda: self.context.scenes.switch("level_select")),
        ]

    def handle_event(self, event):
        for widget in self.widgets:
            if widget.handle_event(event):
                return

    def update(self, dt):
        for widget in self.widgets:
            widget.update(dt)

    def draw(self, surface):
        theme = self.context.themes.current_theme
        surface.fill(theme.sky)
        for widget in self.widgets:
            widget.draw(surface, theme)
