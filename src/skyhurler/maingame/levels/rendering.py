import pygame
from pygame.math import Vector2

from skyhurler.core import settings
from skyhurler.core.fonts import get_font
from skyhurler.ui.HUD import draw_hud

''' Functions for drawing the level scene. This is separate from the LevelScene class'''
def draw_level(scene, surface):
    if scene.level is None:
        return
    theme = scene.context.themes.current_theme
    d = scene.level.defn
    surface.fill(theme.sky)

    if d.wind is not None:
        font = get_font(20)
        direction = ">>>" if d.wind[0] > 0 else "<<<"
        text = font.render(f"WIND {direction}", True, theme.text_dim)
        surface.blit(text, (14, 70))

    for zone_rect, _ in d.friction_zones:
        overlay = pygame.Surface(zone_rect.size, pygame.SRCALPHA)
        overlay.fill((60, 45, 25, 160))
        surface.blit(overlay, zone_rect.topleft)

    pygame.draw.rect(surface, theme.ground, scene.level.ground_rect)

    for obstacle in scene.level.obstacles:
        obstacle.draw(surface, theme)
    for enemy in scene.level.enemies:
        enemy.draw(surface, theme)
    for spent in scene.settled:
        spent.draw(surface, theme)
    for live in scene.level.live_projectiles:
        live.draw(surface, theme)
    scene.vfx.draw(surface)

    _draw_slingshot(scene, surface, theme)

    draw_hud(surface, theme, scene.level, scene.tracker,
             scene.context.selected_character.name)


def _draw_slingshot(scene, surface, theme):
    anchor = Vector2(scene.level.defn.launch_pos)

    pygame.draw.rect(surface, (110, 80, 50),
                     (anchor.x - 6, anchor.y - 10, 12, 110),
                     border_radius=4)
    pygame.draw.circle(surface, (110, 80, 50), (int(anchor.x),
                                                int(anchor.y - 8)), 12)
    ball = scene.sling.loaded
    if ball is None:
        if scene.level.projectiles_remaining > 0:
            pygame.draw.circle(surface, theme.text_dim,
                               (int(anchor.x + 34), int(anchor.y + 60)),
                               14, 2)
        return
    pos = Vector2(anchor)
    if scene.sling.dragging:
        pos = scene.sling.drag_pos
        pull = pos - anchor
        if pull.length() > settings.Drag_radius:
            pull.scale_to_length(settings.Drag_radius)
            pos = anchor + pull
        _draw_preview(scene, surface, theme, anchor - pos)
    for tip in ((anchor.x - 14, anchor.y - 12), (anchor.x + 14, anchor.y - 12)):
        pygame.draw.line(surface, (90, 60, 40), tip,
                         (int(pos.x), int(pos.y)), 5)
    ball.position.update(pos)
    ball.draw(surface, theme)


def _draw_preview(scene, surface, theme, drag_vector):
    velocity = Vector2(drag_vector)
    if velocity.length() > settings.Drag_radius:
        velocity.scale_to_length(settings.Drag_radius)
    velocity = velocity * -settings.Power_scale
    if velocity.length() > settings.Max_launch_power:
        velocity.scale_to_length(settings.Max_launch_power)
    velocity = velocity * scene.context.selected_character.launch_power

    position = Vector2(scene.level.defn.launch_pos)
    gravity = Vector2(settings.Gravity)
    for i in range(settings.Trajectory_steps):
        velocity += gravity * settings.Fixed_dt
        position += velocity * settings.Fixed_dt
        if i % 3 == 0:
            pygame.draw.circle(surface, theme.text_dim,
                               (int(position.x), int(position.y)), 3)
