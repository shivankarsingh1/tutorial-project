import pygame


class AudioManager:
    '''plays the music and sound effects with the saved volume and mute'''

    def __init__(self, resources=None, settings_store=None):
        self._resources = resources
        self._settings = settings_store
        self._available = pygame.mixer.get_init() is not None
        self.muted = settings_store.muted if settings_store is not None else False
        self._volume = settings_store.volume if settings_store is not None else 0.8
        self.start_music()

    def start_music(self):
        '''does nothing if the music cant be loaded or played'''
        if not self._available or self._resources is None:
            return
        path = self._resources.music_path("music_loop")
        if path is None:
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(self._effective_volume())
            pygame.mixer.music.play(loops=-1)
        except pygame.error:
            pass

    def _effective_volume(self):
        return 0.0 if self.muted else self._volume

    def _apply_volume(self):
        if self._available:
            pygame.mixer.music.set_volume(self._effective_volume())

    def toggle_mute(self):
        '''flips mute on and off and saves it'''
        self.muted = not self.muted
        if self._settings is not None:
            self._settings.set_muted(self.muted)
        self._apply_volume()
        return self.muted

    def set_volume(self, volume):
        '''sets the volume and saves it'''
        self._volume = volume
        if self._settings is not None:
            self._settings.set_volume(self._volume)
        self._apply_volume()
        return self._volume

    def play_sfx(self, name):
        '''plays one of the named sound effects if we are not muted'''
        if not self._available or self.muted or self._resources is None:
            return
        sound = self._resources.get_sound(name)
        if sound is None:
            return
        sound.set_volume(self._volume)
        sound.play()
