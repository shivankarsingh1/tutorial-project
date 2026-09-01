
import json
from pathlib import Path

from skyhurler.core import settings

NUM_LEVELS = 4


class SettingsStore:
    '''the apps settings like theme and volume, saved to settings.json'''

    def __init__(self, directory=None):
        if directory is None:
            directory = settings.User_data_dir
        self.path = Path(directory) / "settings.json"

        # defaults, get overwritten if the save file has a value for them
        self.theme = "dark"
        self.muted = False
        self.volume = 0.8

        if self.path.exists():
            try:
                with open(self.path) as f:
                    data = json.load(f)
            except Exception:
                data = {}
            if "theme" in data:
                self.theme = data["theme"]
            if "muted" in data:
                self.muted = data["muted"]
            if "volume" in data:
                self.volume = data["volume"]

        # stop a dodgy save file giving a volume outside 0..1
        if self.volume < 0:
            self.volume = 0.0
        if self.volume > 1:
            self.volume = 1.0

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump({
                "theme": self.theme,
                "muted": self.muted,
                "volume": self.volume,
            }, f)

    def set_muted(self, muted):
        self.muted = muted
        self._save()

    def set_volume(self, volume):
        if volume < 0:
            volume = 0.0
        if volume > 1:
            volume = 1.0
        self.volume = volume
        self._save()

    def set_theme(self, theme):
        self.theme = theme
        self._save()

class ProgressStore:
    '''keeps track of which levels are done and the total score earned,
    saved to progress.json so unlocks still work after the game closes'''

    def __init__(self, directory=None):
        if directory is None:
            directory = settings.User_data_dir
        self.path = Path(directory) / "progress.json"

        self.completed_levels = []
        self.total_score_earned = 0

        if self.path.exists():
            try:
                with open(self.path) as f:
                    data = json.load(f)
            except Exception:
                data = {}
            if isinstance(data, dict):
                self.completed_levels = data.get("completed_levels", [])
                self.total_score_earned = data.get("total_score_earned", 0)

        # make sure there is always exactly one slot per level, missing ones
        # count as not done
        while len(self.completed_levels) < NUM_LEVELS:
            self.completed_levels.append(False)
        if len(self.completed_levels) > NUM_LEVELS:
            self.completed_levels = self.completed_levels[:NUM_LEVELS]

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump({
                "completed_levels": self.completed_levels,
                "total_score_earned": self.total_score_earned,
            }, f)

    def credit_run(self, score, multiplier):
        '''adds the score from a finished run onto the total used for unlocks'''
        self.total_score_earned += int(score * multiplier)
        self._save()

    def is_level_unlocked(self, level_number):
        '''level 1 is always open, the rest need the one before done first'''
        if level_number <= 1:
            return True
        return self.completed_levels[level_number - 2]

    def complete_level(self, level_number):
        '''marks a level as done and saves'''
        slot = level_number - 1
        if not self.completed_levels[slot]:
            self.completed_levels[slot] = True
            self._save()


class ScoreStore:
    '''saves the best scores to scores.json'''

    def __init__(self, directory=None):
        if directory is None:
            directory = settings.User_data_dir
        self.path = Path(directory) / "scores.json"

        self.high_scores = {}
        if self.path.exists():
            try:
                with open(self.path) as f:
                    data = json.load(f)
            except Exception:
                data = {}
            if isinstance(data, dict):
                self.high_scores = data

    def _key(self, game, difficulty):
        return f"{game}:{difficulty}"

    def submit(self, game, score, difficulty="standard"):
        '''saves the score if its a new best, gives back True if it was'''
        key = self._key(game, difficulty)
        if score > self.high_scores.get(key, 0):
            self.high_scores[key] = score
            self._save()
            return True
        return False

    def best(self, game, difficulty="standard"):
        return self.high_scores.get(self._key(game, difficulty), 0)

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.high_scores, f)
