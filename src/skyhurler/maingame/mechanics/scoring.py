from skyhurler.core import settings


class ScoreTracker:

    def __init__(self):
        self.current_score = 0
        self.bonus_points = 0

    def add_enemy_points(self, enemy):
        self.current_score += enemy.points

    def add_obstacle_points(self, obstacle):
        self.current_score += obstacle.material.points

    def add_bonus(self, projectiles_remaining):
        self.bonus_points = projectiles_remaining * settings.Remaining_projectile_bonus

    @property
    def final_score(self):
        return self.current_score + self.bonus_points
