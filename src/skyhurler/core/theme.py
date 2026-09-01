class Theme:
    '''one colour scheme for the whole app'''

    def __init__(self, name, sky, ground, panel, panel_border, text,
                 text_dim, accent, danger, good):
        self.name = name
        self.sky = sky
        self.ground = ground
        self.panel = panel
        self.panel_border = panel_border
        self.text = text
        self.text_dim = text_dim
        self.accent = accent
        self.danger = danger
        self.good = good


DARK_THEME = Theme(
    name="dark",
    sky=(24, 30, 48),
    ground=(52, 60, 74),
    panel=(34, 40, 58),
    panel_border=(90, 102, 130),
    text=(235, 238, 245),
    text_dim=(140, 150, 170),
    accent=(120, 200, 255),
    danger=(235, 90, 90),
    good=(110, 220, 130),
)

LIGHT_THEME = Theme(
    name="light",
    sky=(200, 226, 245),
    ground=(150, 165, 140),
    panel=(238, 242, 248),
    panel_border=(130, 140, 160),
    text=(30, 34, 44),
    text_dim=(110, 118, 132),
    accent=(30, 110, 200),
    danger=(190, 40, 40),
    good=(30, 140, 60),
)

THEMES = {"dark": DARK_THEME, "light": LIGHT_THEME}


class ThemeManager:
    '''remembers which theme is on and swaps it, the saved theme gets read
    at start up so the very first frame drawn has the right colours'''

    def __init__(self, settings_store):
        self._settings = settings_store
        name = settings_store.theme
        if name not in THEMES:
            # saved name isnt a real theme, fall back to dark
            name = "dark"
        self.current_theme = THEMES[name]

    def set_theme(self, name):
        '''switches the theme and saves it so it sticks next launch'''
        if name not in THEMES:
            return
        self.current_theme = THEMES[name]
        self._settings.set_theme(name)

    def toggle(self):
        '''flips between dark and light'''
        if self.current_theme.name == "dark":
            self.set_theme("light")
        else:
            self.set_theme("dark")
