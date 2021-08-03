import ctypes
import cfg
from os import chdir
import entities
import player_input as pinput
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

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    # draw stuff
    main_surf.fill("BLACK")
    player_surf.fill("GREEN")
    main_surf.blit(player_surf, (player.x_pos, player.y_pos))

    for enemy in entities.Enemy.existing_enemies:
        enemy.surface.fill("RED")
        main_surf.blit(enemy.surface, (enemy.x_pos, enemy.y_pos))

    pg.display.flip()

    # movement logic
    move_distance = pinput.get_distance_from_keys_pressed()
    collision_cause = player.seek_possible_collision(move_distance)
    if collision_cause is None:
        player.x_pos += move_distance
    else:
        player.x_pos += player.get_distance_to(collision_cause)

    clock.tick(cfg.FPS)















