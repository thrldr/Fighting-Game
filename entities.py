import cfg
import pygame as pg


class Movable:
    x_pos = 0
    y_pos = 0
    width = 50
    height = 50

    def __init__(self, x=100, y=cfg.FLOOR, w=50, h=50):
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h

    def get_pos(self):
        return self.x_pos, self.y_pos

    def set_pos(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def does_collide(self, target):
        if self.x_pos >= target.x_pos:
            if target.x_pos + target.width >= self.x_pos:
                return True
        elif self.x_pos + self.width >= target.x_pos:
            return True
        return False

    def will_collide(self, step):
        for target in Enemy.existing_enemies:
            if step > 0 and self.x_pos < target.x_pos <= self.x_pos + self.width + step:
                return True
            if step < 0 and target.x_pos < self.x_pos <= target.x_pos + target.width - step:
                return True
        return False

    def get_distance_to(self, target):
        if self.x_pos < target.x_pos:
            return target.x_pos - self.x_pos - self.width
        else:
            return target.x_pos + target.width - self.x_pos


class Enemy(Movable):
    existing_enemies = list()
    HP = cfg.FULL_HP
    surface = pg.Surface((50, 50))

    def __init__(self, size=cfg.ENEMY_SIZE, *args):
        Movable.__init__(self, *args)
        Enemy.existing_enemies.append(self)
        surface = pg.Surface((size, size))

