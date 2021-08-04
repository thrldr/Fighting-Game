import entities
import cfg
import pygame as pg


def game_over(main_surf):
    for entity in entities.Living.entities_list:
        entity.die()
    arial_font = pg.font.SysFont('Impact', 70)
    game_over_text = arial_font.render("GAME OVER", 1, "RED", "YELLOW")
    pos = game_over_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2))
    main_surf.fill("WHITE")
    main_surf.blit(game_over_text, pos)
    pg.display.update()
    return False
