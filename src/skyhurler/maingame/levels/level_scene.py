import pygame

from skyhurler.core import settings
from skyhurler.core.Scene import Scene
from skyhurler.maingame.characters.enemy import Skitterer
from skyhurler.maingame.levels.impact import ImpactResolver
from skyhurler.maingame.levels.level_registry import make_level
from skyhurler.maingame.levels.rendering import draw_level
from skyhurler.maingame.levels.slingshot import Slingshot
from skyhurler.maingame.levels.finished_projectile import FinishedProjectile
from skyhurler.maingame.mechanics.projectile import Projectile
from skyhurler.maingame.mechanics.scoring import ScoreTracker
from skyhurler.maingame.mechanics.vfx import ParticleSystem
from skyhurler.physics.engine import PhysicsEngine
from skyhurler.maingame.characters.character import ROCKO

'''Scene for a level in the game'''
class LevelScene(Scene):

    def __init__(self, context):
        super().__init__(context)
        self.level = None
        self.engine = None
        self.tracker = None
        self.vfx = ParticleSystem()
        self.sling = None
        self.settled = []  # spent balls left lying around
        self.finished = False
        self.enrage_applied = False
        self.impact = ImpactResolver(self)

    def enter(self):
        self.level = make_level(self.context.current_level)
        self.sling = Slingshot(self.level)
        self.tracker = ScoreTracker()
        self.vfx = ParticleSystem()
        self.settled = []
        self.finished = False
        self.enrage_applied = False
        self._build_engine()
        if self.context.selected_character is None:
            self.context.selected_character = ROCKO
            self.context.scenes.push("character_select")

    def _build_engine(self):
        self.engine = PhysicsEngine()
        self.engine.add_responder(self.impact.on_hit)
        self.vfx.bind(self.engine)
        d = self.level.defn
        if d.wind is not None:
            self.engine.add_field(
                pygame.Rect(0, 0, settings.World_width, settings.World_height),
                d.wind,
            )
        for rect, coefficient in d.friction_zones:
            self.engine.add_drag(pygame.Rect(rect), coefficient)

    def handle_event(self, event):
        if self.finished or self.level is None:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.sling.dragging:
                self.sling.cancel()
            else:
                self.context.scenes.push("pause")
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._left_click(event.pos)
            elif event.button == 3 and self.sling.dragging:
                self.sling.cancel()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.sling.dragging:
                self._release()
        elif event.type == pygame.MOUSEMOTION and self.sling.dragging:
            self.sling.drag_pos.update(event.pos)

    def _left_click(self, pos):
        if self.sling.loaded is None:
            for p in self.level.live_projectiles:
                if p.is_splitter and not p.has_collided and not p.at_rest():
                    self._split(p)
                    return
        character = self.context.selected_character
        sprite = self.context.resources.loaded_images.get(
            character.name.lower())
        self.sling.grab(pos, character, sprite)

    def _release(self):
        drag = self.sling.release()
        if drag is None:
            return
        ball = self.sling.loaded
        ball.launch(drag)
        ball.register_with(self.engine, self.level.enemies,
                           self.level.obstacles, self.level.ground_rect)
        self.context.audio.play_sfx("launch")
        self.sling.loaded = None

    def _split(self, parent):
        self.engine.remove_body(parent)
        self.level.live_projectiles.remove(parent)
        for angle in (-settings.Split_spread_degrees, 0.0,
                      settings.Split_spread_degrees):
            child = Projectile(parent.character, parent.position,
                               sprite=parent.sprite)
            child.velocity = parent.velocity.rotate(angle)
            child.mass = parent.mass * settings.Split_child_mass_fraction
            child.radius = parent.radius * settings.Split_child_radius_fraction
            child.register_with(self.engine, self.level.enemies,
                                self.level.obstacles, self.level.ground_rect)
            self.level.live_projectiles.append(child)
        self.vfx.burst(parent.position, parent.character.color, 12,
                       speed=160.0, lifetime=0.4)
        self.context.audio.play_sfx("launch")

    def update(self, dt):
        if self.finished or self.level is None:
            return
        self.engine.step(dt)
        for enemy in self.level.enemies:
            enemy.update(dt)
        self._apply_enrage()
        for spent in self.level.clear_settled_projectiles():
            self.engine.remove_body(spent)
            self.settled.append(FinishedProjectile(spent))
        for spent in self.settled:
            spent.tick(dt)
        self.settled = [spent for spent in self.settled if spent.visible]
        self.vfx.prune()
        self._check_outcome()

    def _apply_enrage(self):
        boss = self.level.boss()
        if (boss is not None and boss.alive and boss.enraged
                and not self.enrage_applied):
            for enemy in self.level.enemies:
                if isinstance(enemy, Skitterer):
                    enemy.speed *= 2
            self.enrage_applied = True
            self.vfx.burst(boss.position, boss.color, 26, speed=300,
                           lifetime=1.0)

    def _check_outcome(self):
        if self.level.is_complete():
            self._finish(won=True)
        elif self.level.has_failed():
            self._finish(won=False)

    def _finish(self, won):
        self.finished = True
        if won:
            self.tracker.add_bonus(self.level.projectiles_remaining)
            self.context.progress.complete_level(self.level.index)
        self.context.last_result = {
            "won": won,
            "level_index": self.level.index,
            "level_name": self.level.defn.name,
            "score": self.tracker.current_score,
            "bonus": self.tracker.bonus_points,
            "final": self.tracker.final_score,
        }
        self.context.audio.play_sfx("win" if won else "lose")
        self.context.scenes.switch("result")

    def draw(self, surface):
        draw_level(self, surface)
