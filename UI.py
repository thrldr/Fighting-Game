import cfg
import pygame as pg


def draw_hp(surface, player_hp, enemy_hp):
    small_impact_font = pg.font.SysFont('Arial', 60)

    player_hp_text = small_impact_font.render(str(player_hp), 1, "WHITE")
    player_hp_pos = player_hp_text.get_rect(topleft=(100, 40))
    surface.blit(player_hp_text, player_hp_pos)

    enemy_hp_text = small_impact_font.render(str(enemy_hp), 1, "WHITE")
    enemy_hp_pos = enemy_hp_text.get_rect(topright=(cfg.DISPLAY_X - 100, 40))
    surface.blit(enemy_hp_text, enemy_hp_pos)


def draw_fighting_image_on(surface):
    image_surface = pg.image.load("resources/fight.bmp")
    image_rect = image_surface.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 - 170))
    surface.blit(image_surface, image_rect)


def draw_victory_screen_on(surface):
    surface.fill(cfg.BG_COLOR)

    small_impact_font = pg.font.SysFont('Arial', 30)
    restart_text = small_impact_font.render("press Enter to restart", 1, "BLACK")
    restart_pos = restart_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 200))
    surface.blit(restart_text, restart_pos)

    impact_font = pg.font.SysFont('Impact', 90)
    end_text = "YOU WIN"
    game_over_text = impact_font.render(end_text, 1, "RED", cfg.TEXT_BG_COLOR)
    game_over_pos = game_over_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 100))
    surface.blit(game_over_text, game_over_pos)

    image_surface = pg.image.load("resources/crown.bmp")
    image_rect = image_surface.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 - 150))
    surface.blit(image_surface, image_rect)


def draw_defeat_screen_on(surface):
    surface.fill(cfg.BG_COLOR)

    small_impact_font = pg.font.SysFont('Arial', 30)
    restart_text = small_impact_font.render("press Enter to restart", 1, "BLACK")
    restart_pos = restart_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 200))
    surface.blit(restart_text, restart_pos)

    impact_font = pg.font.SysFont('Impact', 90)
    end_text = "GAME OVER"
    game_over_text = impact_font.render(end_text, 1, "RED", cfg.TEXT_BG_COLOR)
    game_over_pos = game_over_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 100))
    surface.blit(game_over_text, game_over_pos)

    image_surface = pg.image.load("resources/dead.bmp")
    image_rect = image_surface.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 - 150))
    surface.blit(image_surface, image_rect)
