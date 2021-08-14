import pygame as pg
import game_cycle
import cfg


def input_placeholder(player):
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_x:
            player.shoot()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            return False
        if event.type == pg.QUIT:
            exit()
    return True


def get_distance_from_keys_pressed():
    pressed_keys = pg.key.get_pressed()
    if pressed_keys[pg.K_LEFT]:
        return -cfg.MOVE_SPEED
    elif pressed_keys[pg.K_RIGHT]:
        return cfg.MOVE_SPEED
    else:
        return 0
