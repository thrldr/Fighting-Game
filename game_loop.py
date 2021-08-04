import cfg
import cx_Freeze
from os import chdir
import game_logic
import pygame as pg
pg.init()

# initializing board
chdir(r"C:/Users/thrldr/Desktop/res")
pg.display.set_caption("scaffolding")
pg.display.set_icon(pg.image.load("icon.bmp"))
clock = pg.time.Clock()

main_surf = pg.display.set_mode((cfg.DISPLAY_X, cfg.DISPLAY_Y))

# main menu
continue_loop = True
main_menu = game_logic.Menus("New Game", "Options", "Exit")
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        main_menu.read_controls(event, main_surf, clock)
    main_menu.show_on(main_surf)
    image_surface = pg.image.load("fight.bmp")
    image_rect = image_surface.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 - 170))
    main_surf.blit(image_surface, image_rect)
    pg.display.update()
    clock.tick(cfg.FPS)

