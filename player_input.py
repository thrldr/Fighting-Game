import pygame as pg
import entities
import cfg


def input_placeholder(*args):
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_x:
            args[0].shoot()
        if event.type == pg.QUIT:
            exit()


def get_distance_from_keys_pressed():
    pressed_keys = pg.key.get_pressed()
    if pressed_keys[pg.K_LEFT]:
        return -cfg.MOVE_SPEED
    elif pressed_keys[pg.K_RIGHT]:
        return cfg.MOVE_SPEED
    else:
        return 0
