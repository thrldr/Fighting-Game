import cfg
import pygame as pg


def draw_fighting_image_on(surface):
    image_surface = pg.image.load("resources/fight.bmp")
    image_rect = image_surface.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 - 170))
    surface.blit(image_surface, image_rect)


def draw_game_over_screen_on(surface):
    surface.fill(cfg.BG_COLOR)

    small_impact_font = pg.font.SysFont('Arial', 30)
    restart_text = small_impact_font.render("press Enter to restart", 1, "BLACK")
    restart_pos = restart_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 200))
    surface.blit(restart_text, restart_pos)

    impact_font = pg.font.SysFont('Impact', 90)
    game_over_text = impact_font.render("GAME OVER", 1, "RED", cfg.TEXT_BG_COLOR)
    game_over_pos = game_over_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 100))
    surface.blit(game_over_text, game_over_pos)

    image_surface = pg.image.load("resources/dead.bmp")
    image_rect = image_surface.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 - 150))
    surface.blit(image_surface, image_rect)
