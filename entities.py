import cfg
import pygame as pg


class Movable:
    def __init__(self, x, y, w=50, h=50, color="YELLOW"):
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h
        self.direction = "RIGHT"
        self.surface = pg.Surface((w, h))
        self.color = color

    def get_direction(self):
        return self.direction

    def set_direction(self, vector):
        if vector < 0:
            self.direction = "LEFT"
        elif vector > 0:
            self.direction = "RIGHT"

    def get_pos(self):
        return self.x_pos, self.y_pos

    def set_pos(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def is_collided(self, target):
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

    def __init__(self, *args, hp=100, **kwargs):
        Movable.__init__(self, *args, **kwargs)
        self.HP = hp
        Living.entities_list.append(self)

    def die(self):
        if self in Living.entities_list:
            Living.entities_list.remove(self)
        del self


class Player(Living):
    is_dead = False

    def jump(self):
        self.jump_buffer = self.y_pos

    def die(self):
        self.is_dead = True
        Living.die(self)

    def __init__(self, *args, color="GREEN"):
        Living.__init__(self, *args, color=color)
        self.direction = "RIGHT"
        self.jump_buffer = cfg.FLOOR

    def calculate_projectile_starting_point(self):
        if self.direction == "LEFT":
            return self.x_pos - cfg.PROJECTILE_WIDTH, self.y_pos + 15
        else:
            return self.x_pos + self.width, self.y_pos + 15

    def hit(self):
        starting_point = self.calculate_projectile_starting_point()
        Limb(self.direction, *starting_point)

    def shoot(self):
        starting_point = self.calculate_projectile_starting_point()
        Projectile(self.direction, *starting_point)


class Enemy(Living):
    existing_enemies = list()

    def __init__(self, *args, color="RED"):
        Living.__init__(self, *args, color=color)
        Enemy.existing_enemies.append(self)

    def rush(self, player):
        if self.x_pos < player.x_pos:
            self.x_pos += cfg.ENEMY_SPEED
        else:
            self.x_pos += -cfg.ENEMY_SPEED

    def die(self):
        if self in Living.entities_list:
            Living.entities_list.remove(self)
            Enemy.existing_enemies.remove(self)
        del self


class Limb(Movable):
    instance = None

    def __init__(self, direction, x, y, proj_with=cfg.PROJECTILE_WIDTH, proj_height=cfg.PROJECTILE_HEIGHT):
        instance = self
        Movable.__init__(self, x, y, proj_with, proj_height)
        self.direction = direction

    def die(self):
        if Limb.instance is not None:
            Limb.instance = None
            del self


class Projectile(Movable):
    existing_projectiles = list()
    surface = pg.Surface((cfg.PROJECTILE_WIDTH, cfg.PROJECTILE_HEIGHT))

    def __init__(self, direction, x, y, proj_with=cfg.PROJECTILE_WIDTH, proj_height=cfg.PROJECTILE_HEIGHT):
        Movable.__init__(self, x, y, proj_with, proj_height)
        self.direction = direction
        Projectile.existing_projectiles.append(self)

    def out_of_display(self):
        return self.x_pos < 0 or self.x_pos > cfg.DISPLAY_X

    def die(self):
        if self in Projectile.existing_projectiles:
            Projectile.existing_projectiles.remove(self)
        del self
