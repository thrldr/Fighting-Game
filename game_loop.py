import ctypes
import cfg
from os import chdir
import entities
import pygame as pg
pg.init()


# initializing board
chdir(r"C:/Users/thrldr/Desktop/res")
user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pg.display.set_caption("scaffolding")
pg.display.set_icon(pg.image.load("icon.bmp"))

main_surf = pg.display.set_mode((600, 400))
player_surf = pg.Surface((50, 50))

clock = pg.time.Clock()

player = entities.Movable(200, cfg.FLOOR)
enemy1 = entities.Enemy(50, 450, cfg.FLOOR)
enemy2 = entities.Enemy(50, 100, cfg.FLOOR)

# Game Loop
continue_loop = True
while continue_loop:

    main_surf.fill("BLACK")
    for enemy in entities.Enemy.existing_enemies:
        enemy.surface.fill("RED")
        main_surf.blit(enemy.surface, (enemy.x_pos, enemy.y_pos))

    player_surf.fill("GREEN")
    main_surf.blit(player_surf, (player.x_pos, player.y_pos))

    pg.display.flip()

    # TODO: refactor collisions and separate controller
    pressed_keys = pg.key.get_pressed()
    if pressed_keys[pg.K_LEFT]:
        if not player.will_collide(-10):
            player.x_pos -= 15
        else:
            player.x_pos += player.get_distance_to(enemy2)
    elif pressed_keys[pg.K_RIGHT]:
        if not player.will_collide(10):
            player.x_pos += 15
        else:
            player.x_pos += player.get_distance_to(enemy1)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            continue_loop = False

    clock.tick(cfg.FPS)
