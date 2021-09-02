import cfg
import pygame as pg


class Movable(pg.sprite.Sprite):
    instances = list()

    @staticmethod
    def prepare_image(image, dimensions=cfg.FIGHTER_SIZE):
        try:
            img = pg.image.load("resources/sprites/"+image).convert()
            img.set_colorkey("WHITE")
            return pg.transform.scale(img, dimensions)
        except FileNotFoundError:
            return pg.image.load("resources/sprites/no_sprite.png").convert()

    def __init__(self, position, sprite, dimensions=cfg.FIGHTER_SIZE):
        pg.sprite.Sprite.__init__(self)
        self.image_name = sprite
        self.image = Movable.prepare_image(sprite, dimensions)
        self.rect = self.image.get_rect(bottomleft=position)
        self.movement_vector = 0
        self.is_dashing = False
        self.dash_timer = 0
        self.direction = 1

    def set_dash_timer(self, time):
        self.dash_timer = time

    def set_dashing(self):
        self.dash_timer = cfg.DASH_TIME
        self.is_dashing = True

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self.movement_vector


class Status:
    def __init__(self, name):
        self.name = name


class Living(Movable):
    def __init__(self, *args, hp=cfg.FULL_HP, **kwargs):
        super(Living, self).__init__(*args, **kwargs)
        self.health = hp
        self.stamina = 100
        self.balance = 100
        self.is_crouching = False
        self.damage_modifier = 1
        self.statuses = set()
        Movable.instances.append(self)

    def update(self, *args, **kwargs) -> None:
        self.dash_timer_tick()

        if self.is_dashing:
            if self.is_crouching:
                self.movement_vector = cfg.MOVE_SPEED * self.direction * 1.5
            else:
                self.movement_vector = cfg.MOVE_SPEED * self.direction * 2.5
            Movable.update(self)
            return

        if self.is_crouching:
            if self.image_name != "ducked.png":
                self.image_name = "ducked.png"
                height = cfg.FIGHTER_SIZE[1] // 1.5
                self.image = super(Living, self).prepare_image("ducked.png", (cfg.FIGHTER_SIZE[0], int(height)))
                self.rect = self.image.get_rect(bottomleft=(self.rect.x, cfg.FLOOR))
            self.movement_vector //= 2

        elif self.image_name != "right_stance.png":
            self.image_name = "right_stance.png"
            self.image = super(Living, self).prepare_image("right_stance.png", cfg.FIGHTER_SIZE)
            self.rect = self.image.get_rect(bottomleft=(self.rect.x, cfg.FLOOR))

        Movable.update(self)

    def dash_timer_tick(self):
        if self.dash_timer > 0:
            self.dash_timer -= 1
        elif self.is_dashing:
            self.is_dashing = False


class Player(Living):
    pass


class Enemy(Living):
    pass
