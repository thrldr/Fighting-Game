import cfg
import entities
import random


class Enemy_generator:
    @staticmethod
    def generate():
        enemy_side = random.randint(0, 100)
        if enemy_side > 50:
            enemy_start = (100, cfg.FLOOR)
        else:
            enemy_start = (cfg.DISPLAY_X - 150, cfg.FLOOR)
        enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        entities.Enemy(*enemy_start, color=enemy_color)

