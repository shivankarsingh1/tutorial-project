from pathlib import Path

import pygame

Default_Assets_Dir = Path(__file__).resolve().parents[1] / "assets"
'''default folder  location for all game assets'''

class ResourceManager:

    ''' uses the given asset folder if its provided otherwises uses default one'''
    def __init__(self, assets_dir = None):
        if assets_dir:
            self.assets_dir = Path(assets_dir)
        else:
            self.assets_dir = Default_Assets_Dir
        self.loaded_images = {}
        self.loaded_sounds = {}
        self.loaded_fonts = {}

        pygame.font.init()
        self._load_all()

    '''loads all images and sounds which are found in the assets folder automatically'''
    def _load_all(self):
        images_dir = self.assets_dir / "images"
        sounds_dir = self.assets_dir / "sounds"
        if images_dir.is_dir():
            for path in sorted(images_dir.iterdir()):
                if path.suffix.lower() == ".png":
                    self._load_image(path.stem, path)
        if sounds_dir.is_dir():
            for path in sorted(sounds_dir.iterdir()):
                if path.suffix.lower() == ".wav":
                    self._load_sound(path.stem, path)
    
    
    def _load_image(self, name, path):
        try:
            self.loaded_images[name] = pygame.image.load(str(path))
        except (pygame.error, FileNotFoundError):
            pass

    def _load_sound(self, name, path):
        try:
            self.loaded_sounds[name] = pygame.mixer.Sound(str(path))
        except Exception:
            pass

    def music_path(self, name="music_loop"):

        """Full path of a music file, or None if it isn't there."""
        path = self.assets_dir / "sounds" / f"{name}.wav"
        return path if path.exists() else None

    def get_sound(self, name):
        return self.loaded_sounds.get(name)