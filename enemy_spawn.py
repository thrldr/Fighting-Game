import cfg
import entities
import random


def clear_board():
    while len(entities.Projectile.existing_projectiles) > 0:
        for bullet in entities.Projectile.existing_projectiles:
            bullet.die()
    while len(entities.Living.entities_list) > 0:
        for entity in entities.Living.entities_list:
            entity.die()


class Enemy_spawner:
    @staticmethod
    def spawn():
        enemy_side = random.randint(0, 100)
        if enemy_side > 50:
            enemy_start = (-50, cfg.FLOOR)
        else:
            enemy_start = (cfg.DISPLAY_X + 50, cfg.FLOOR)
        enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        entities.Enemy(*enemy_start, color=enemy_color)

