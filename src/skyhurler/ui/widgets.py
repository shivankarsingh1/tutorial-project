from abc import ABC, abstractmethod
import pygame

from skyhurler.core.fonts import get_font

'''base class for all widgets in the game'''
class Widget(ABC):
    '''base class for button and other ui thins'''

    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.visible = True

    def update(self, dt):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def draw(self, surface, theme):
        pass


class Button(Widget):

    def __init__(self, rect, text, on_click=None, font_size=26, enabled=True):
        super().__init__(rect)
        self.text = text
        self.on_click = on_click
        self.font_size = font_size
        self.enabled = enabled

    def handle_event(self, event):
        if not self.visible or not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click is not None:
                    self.on_click()
                return True
        return False

    def draw(self, surface, theme):
        if not self.visible:
            return
        pygame.draw.rect(surface, (80, 80, 80), self.rect)
        font = get_font(self.font_size)
        lines = self.text.split("\n")
        line_h = font.size("Ag")[1] + 2
        y = self.rect.centery - line_h * len(lines) / 2 + line_h / 2
        for line in lines:
            label = font.render(line, True, (255, 255, 255))
            surface.blit(label, label.get_rect(center=(self.rect.centerx, y)))
            y += line_h


class Label(Widget):
    '''plain text in the middle of its rect'''

    def __init__(self, rect, text="", font_size=24):
        super().__init__(rect)
        self.text = text
        self.font_size = font_size

    def handle_event(self, event):
        return False   # labels never consume events

    def draw(self, surface, theme):
        if not self.visible or not self.text:
            return
        font = get_font(self.font_size)
        label = font.render(self.text, True, theme.text)
        surface.blit(label, label.get_rect(center=self.rect.center))
