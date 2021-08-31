import pygame as pg
import game_states
import cfg


def get_distance_from_keys_pressed():
    pressed_keys = pg.key.get_pressed()
    if pressed_keys[pg.K_LEFT]:
        return -cfg.MOVE_SPEED
    elif pressed_keys[pg.K_RIGHT]:
        return cfg.MOVE_SPEED
    else:
        return 0
