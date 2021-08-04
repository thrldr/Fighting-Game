import cfg
import pygame as pg


class Movable:
    x_pos = 0
    y_pos = 0
    width = 50
    height = 50
    direction = "CENTER"  # supported directions: LEFT, RIGHT, CENTER

    def get_direction(self):
        return self.direction

    def set_direction(self, vector):
        if vector > 0:
            self.direction = "LEFT"
        elif vector < 0:
            self.direction = "RIGHT"

    def __init__(self, x=100, y=cfg.FLOOR, w=50, h=50):
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h
        self.direction = "CENTER"

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

    def seek_possible_collision(self, step):
        for target in Enemy.existing_enemies:
            if step > 0 and self.x_pos < target.x_pos <= self.x_pos + self.width + step:
                return target
            if step < 0 and target.x_pos < self.x_pos <= target.x_pos + target.width - step:
                return target
        return None

    def get_distance_to(self, target):
        if self.x_pos < target.x_pos:
            return target.x_pos - self.x_pos - self.width
        else:
            return target.x_pos + target.width - self.x_pos


class Living(Movable):
    entities_list = list()
    HP = cfg.FULL_HP
    surface = pg.Surface((50, 50))

    def die(self):
        print(Living.entities_list)
        if self in Living.entities_list:
            Living.entities_list.remove(self)
        del self

    def __init__(self, size=cfg.ENEMY_SIZE, *args, hp=100):
        Movable.__init__(self, *args)
        self.HP = hp
        Living.entities_list.append(self)
        surface = pg.Surface((size, size))


class Player(Living):
    color = "GREEN"

    def __init__(self, *args):
        Living.__init__(self, *args)


class Enemy(Living):
    color = "RED"
    existing_enemies = list()

    def die(self):
        Enemy.existing_enemies.remove(self)
        del self

    def __init__(self, *args):
        Living.__init__(self, *args)
        Enemy.existing_enemies.append(self)



