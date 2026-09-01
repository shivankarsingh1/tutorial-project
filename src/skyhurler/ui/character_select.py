import pygame

from skyhurler.core.Scene import Scene
from skyhurler.core.fonts import get_font
from skyhurler.core.theme import THEMES
from skyhurler.maingame.characters.character import CHARACTERS
from skyhurler.ui.widgets import Button

def _wrap_text(text, font, max_width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if font.size(trial)[0] <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

''' A scene for selecting a character. '''
class CharacterSelectScene(Scene):

    def enter(self):
        progress = self.context.progress
        total_score_earned = progress.total_score_earned if progress else 0
        self.cards = [
            (character, pygame.Rect(140 + i * 340, 180, 300, 340),
             character.is_unlocked(total_score_earned))
            for i, character in enumerate(CHARACTERS)
        ]
        self.back = Button((540, 600, 200, 46), "Back",
                           self.context.scenes.pop)

    def handle_event(self, event):
        ctx = self.context
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            ctx.scenes.pop()
            return
        if self.back.handle_event(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for character, rect, unlocked in self.cards:
                if unlocked and rect.collidepoint(event.pos):
                    ctx.selected_character = character
                    ctx.audio.play_sfx("ui_click")
                    ctx.scenes.switch(f"level{ctx.current_level}")
                    return

    def update(self, dt):
        pass

    def draw(self, surface):
        theme = THEMES["dark"]
        surface.fill(theme.sky)
        title = get_font(44).render(
            "Choose your Character", True, theme.text)
        surface.blit(title, title.get_rect(center=(640, 80)))

        font = get_font(26)
        small = get_font(18)
        for character, rect, unlocked in self.cards:
            body = theme.panel if unlocked else (40, 42, 50)
            if not unlocked:
                border = theme.panel_border
            elif character is self.context.selected_character:
                border = theme.accent
            else:
                border = theme.good
            pygame.draw.rect(surface, body, rect, border_radius=10)
            pygame.draw.rect(surface, border, rect, width=3, border_radius=10)

            sprite = self.context.resources.loaded_images.get(
                character.name.lower())
            if sprite is not None:
                sprite = pygame.transform.smoothscale(sprite, (96, 96))
                if not unlocked:
                    sprite = sprite.copy()
                    sprite.set_alpha(110)
                surface.blit(sprite, sprite.get_rect(
                    center=(rect.centerx, rect.top + 90)))

            if not unlocked:
                lock = small.render(
                    f"Unlocks at {character.unlock_score} pts", True,
                    theme.danger)
                surface.blit(lock, lock.get_rect(
                    center=(rect.centerx, rect.bottom - 30)))
                continue

            name = font.render(character.name, True, theme.text)
            surface.blit(name, name.get_rect(
                center=(rect.centerx, rect.top + 170)))

            y = rect.top + 205
            for line in _wrap_text(character.ability, small, rect.width - 24):
                ability_surf = small.render(line, True, theme.text_dim)
                surface.blit(ability_surf,
                             ability_surf.get_rect(center=(rect.centerx, y)))
                y += 22

            stats = small.render(character.describe(), True, theme.text_dim)
            surface.blit(stats, stats.get_rect(
                center=(rect.centerx, rect.bottom - 24)))

        self.back.draw(surface, theme)