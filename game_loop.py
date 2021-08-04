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

main_surf = pg.display.set_mode((cfg.DISPLAY_X, cfg.DISPLAY_Y))
# player_surf = pg.Surface((50, 50))

clock = pg.time.Clock()

player = entities.Player(200, cfg.FLOOR)
enemy1 = entities.Enemy(50, 450, cfg.FLOOR)
enemy2 = entities.Enemy(50, 100, cfg.FLOOR)

# Game Loop
continue_loop = True
while continue_loop:

    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_x and enemy1 in entities.Enemy.existing_enemies:
            enemy1.die()
        if event.type == pg.QUIT:
            exit()

    # render stuff
    main_surf.fill("BLACK")
    for entity in entities.Living.entities_list:
        entity.surface.fill(entity.color)
        main_surf.blit(entity.surface, (entity.x_pos, entity.y_pos))
    pg.display.flip()

    # movement logic
    move_vector = pinput.get_distance_from_keys_pressed()
    player.set_direction(move_vector)

    collision_cause = player.seek_possible_collision(move_vector)
    if collision_cause is None:
        player.x_pos += move_vector
    else:
        player.x_pos += player.get_distance_to(collision_cause)

    clock.tick(cfg.FPS)

