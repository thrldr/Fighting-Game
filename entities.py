import cfg
import pygame as pg


class Movable(pg.sprite.Sprite):
    instances = list()

    def __init__(self, position, dimensions=cfg.FIGHTER_SIZE, sprite="no_sprite.png"):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("resources/sprites/"+sprite).convert()
        self.image = pg.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect(bottomleft=position)

    def update(self, *args, **kwargs) -> None:
        self.rect.x += args[0]


class Living(Movable):
    def __init__(self, *args, hp=cfg.FULL_HP, **kwargs):
        super(Living, self).__init__(*args, **kwargs)
        self.health = hp
        self.stamina = 100
        self.balance = 100
        Movable.instances.append(self)


class Player(Living):
    pass


class Enemy(Living):
    pass
