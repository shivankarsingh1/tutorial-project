import pygame
from skyhurler.assets.audio import AudioManager
from skyhurler.core import settings
from skyhurler.core.resources import ResourceManager
from skyhurler.core.settings_store import SettingsStore, ProgressStore, ScoreStore
from skyhurler.core.theme import ThemeManager
from skyhurler.minigames.minigame_skydice import MinigameSkyDice
from skyhurler.minigames.minigame_skyrunner import MinigameSkyrunner
from skyhurler.ui.character_select import CharacterSelectScene
from skyhurler.ui.main_menu import MainMenu
from skyhurler.ui.level_select import LevelSelect
from skyhurler.ui.option_scene import OptionScene
from skyhurler.ui.pause_overlay import PauseOverlay
from skyhurler.maingame.levels.level_scene import LevelScene
from skyhurler.ui.completion_scene import CompletionScene
from skyhurler.ui.result_scene import ResultScene
''' above are all dependencies for game to run '''

class AppContext:

    def __init__(self):
        self.resources = None
        self.audio = None
        self.themes = None
        self.scores = None
        self.progress = None
        self.settings = None
        self.scenes = None
        self.current_level = 1
        self.selected_character = None
        self.quit_requested = False

class ScenesManager:
    '''' this class manages the scenes and switched when needed, scenes are kept
    in a stack so one can sit ontop of another (the pause menu goes ontop of the level)'''

    def __init__(self, scenes):
        self._scenes = scenes
        self.current = None
        self._stack = []

    def switch(self, key):
        '''goes to a new scene, anything that was stacked before is forgotten'''
        scene = self._scenes[key]
        self._stack = []
        self._stack.append(scene)
        self.current = scene
        self.current.enter()

    def push(self, key):
        '''puts a scene ontop of the stack without getting rid of whats under it,
        the scene pushed becomes the current one and gets enter() called'''
        scene = self._scenes[key]
        self._stack.append(scene)
        self.current = scene
        self.current.enter()

    def pop(self):
        '''takes the top scene off and goes back to the one under it.
        enter() is NOT called on the scene we go back to on purpose, if it was
        then the level would get reset and restart every time the game is unpaused'''
        if len(self._stack) > 1:
            self._stack.pop()
            under = self._stack[-1]
            self.current = under
        # if only one scene is left the pop is just ignored, the stack should
        # never be empty or self.current would be None and update() would crash

    def handle_event(self, event):
        self.current.handle_event(event)

    def update(self, dt):
        self.current.update(dt)

    def draw(self, surface):
        '''draws the whole stack from the bottom up, usually there is only one
        scene in it but when paused the level gets drawn first and then the
        pause menu draws over the top of it'''
        for scene in self._stack:
            scene.draw(surface)


class Game:
    def __init__(self, fullscreen=False):
        pygame.init()
        pygame.display.set_caption('Shivora Games')
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
            ''' if there is no audio the game will still run'''

        ''' sets ups shared system onve and stored on context so tat every scene can access them '''
        self.context = AppContext()

        self.context.resources = ResourceManager()

        self.context.progress = ProgressStore()
        self.context.scores = ScoreStore()


        self.context.settings = SettingsStore()
        self.context.audio = AudioManager(
            self.context.resources, self.context.settings
        )
        self.context.themes = ThemeManager(self.context.settings)
            
        if fullscreen:
            flags = pygame.FULLSCREEN
        else:
            flags = pygame.RESIZABLE | pygame.SCALED

        self.surface = pygame.display.set_mode(settings.World_size, flags)
        self.clock = pygame.time.Clock()

        
        self.scenes = ScenesManager({
            "main_menu": MainMenu(self.context),
            "level_select": LevelSelect(self.context),
            "options": OptionScene(self.context),
            "minigame_skydice": MinigameSkyDice(self.context),
            'minigame_skyrunner': MinigameSkyrunner(self.context),
            "level1": LevelScene(self.context),
            "level2": LevelScene(self.context),
            "level3": LevelScene(self.context),
            "level4": LevelScene(self.context),
            "completion_scene": CompletionScene(self.context),
            "result": ResultScene(self.context),
            "character_select": CharacterSelectScene(self.context),
            "pause": PauseOverlay(self.context),
        })
        self.context.scenes = self.scenes
        '''scenes being registered to the scenes manager '''

    def run(self):
        self.scenes.switch("main_menu")

        while not self.context.quit_requested:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.context.quit_requested = True
                else:
                    self.scenes.handle_event(event)
                    ''' if event not quit passed to scene manager to handle'''
            self.scenes.update(self.clock.tick(settings.FPS) / 1000.0)
            self.scenes.draw(self.surface)
            pygame.display.flip()

        pygame.quit()

