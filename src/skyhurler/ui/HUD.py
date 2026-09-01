import pygame

from skyhurler.core.fonts import get_font

'''draws the bar on the top of the screen wiht the level and character name, 
      score and the number of projectiles remaining'''
def draw_hud(surface , theme, level, tracker, character_name):

    '''SRCALPHA  allows surface to be transparent. '''
    panel = pygame.Surface((surface.get_width(), 46 ), pygame.SRCALPHA)
    panel.fill((10, 12, 18, 150))
    surface.blit(panel, (0, 0))

    font = get_font(22)
    small = get_font(16)

    left = font.render(f"{level.defn.name}", True, theme.text)
    surface.blit(left, (14, 6))
    sub = small.render(f"Character: {character_name}", True, theme.text_dim)
    surface.blit(sub, (14, 26))


    score = font.render(f"Score: {tracker.current_score}", True, theme.text)
    surface.blit(score, (score.get_rect(center=(640, 14))))

    '''draws the number of projectiles remaining on the top right corner of the screen'''
    x = 1266
    for i in range(level.projectiles_remaining):
        pygame.draw.circle(surface, theme.accent, (x, 16), 8)
        x -= 22
    projectile_count = small.render(f"projectiles {level.projectiles_remaining}", True,
                        theme.text_dim)
    surface.blit(projectile_count, (projectile_count.get_rect(topright=(1266, 26))))
