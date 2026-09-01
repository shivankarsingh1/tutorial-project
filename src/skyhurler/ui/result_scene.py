import pygame

from skyhurler.core.Scene import Scene
from skyhurler.core.fonts import get_font
from skyhurler.core.settings_store import NUM_LEVELS
from skyhurler.ui.widgets import Button


class ResultScene(Scene):
    '''shows the score for the run and lets you retry,
    go to the next level or back to the menu'''

    def enter(self):
        context = self.context
        self.result = context.last_result

        r = self.result
        self.new_high = context.scores.submit("skyhurler", r["final"],
                                              difficulty="standard")
        context.progress.credit_run(r["final"], 1)

        next_index = r["level_index"] + 1
        can_continue = (r["won"]
                        and next_index <= NUM_LEVELS
                        and context.progress.is_level_unlocked(next_index))

        def click_then(key):
            '''plays the click sound then switches scene'''
            def on_click():
                context.audio.play_sfx("ui_click")
                context.scenes.switch(key)
            return on_click

        def next_level():
            context.audio.play_sfx("ui_click")
            context.current_level = next_index
            context.scenes.switch(f"level{next_index}")

        self.widgets = [
            Button((440, 430, 180, 50), "Retry",
                   click_then(f"level{context.current_level}")),
        ]
        if can_continue:
            self.widgets.append(
                Button((660, 430, 180, 50), "Next Level", next_level))
        self.widgets.append(Button((540, 500, 200, 50), "Menu",
                                   click_then("main_menu")))

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
        theme = self.context.themes.current_theme
        surface.fill(theme.sky)
        r = self.result

        title_font = get_font(64)
        title = title_font.render(
            "LEVEL COMPLETE!" if r["won"] else "OUT OF PROJECTILES", True,
            theme.good if r["won"] else theme.danger)
        surface.blit(title, title.get_rect(center=(640, 140)))

        font = get_font(30)
        lines = [
            f"{r['level_name']}  (Level {r['level_index']})",
            f"Score: {r['score']}",
            f"Ammo bonus: +{r['bonus']}",
            f"Final score: {r['final']}",
        ]
        y = 230
        for line in lines:
            text = font.render(line, True, theme.text)
            surface.blit(text, text.get_rect(center=(640, y)))
            y += 44

        if self.new_high:
            flash = font.render("NEW HIGH SCORE!", True, theme.accent)
            surface.blit(flash, flash.get_rect(center=(640, y + 16)))

        for widget in self.widgets:
            widget.draw(surface, theme)
