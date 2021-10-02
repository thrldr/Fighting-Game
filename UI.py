import constants as cfg
import pygame as pg


def prepare_image(image, dimensions=cfg.FIGHTER_SIZE):
    try:
        img = pg.image.load("resources/sprites/" + image).convert()
        img.set_colorkey("WHITE")
        return pg.transform.scale(img, dimensions)
    except FileNotFoundError:
        return pg.image.load("resources/sprites/no_sprite.png").convert()


def draw_text(surface, *args):
    small_impact_font = pg.font.SysFont('Arial', 20)

    text = ''
    for arg in args:
        text += str(arg) + '        '
    player_hp_text = small_impact_font.render(str(text), 1, "WHITE")
    player_hp_pos = player_hp_text.get_rect(topleft=(20, 20))
    surface.blit(player_hp_text, player_hp_pos)


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
