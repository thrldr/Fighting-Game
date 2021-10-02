import constants as cfg
import pygame as pg
import UI
from renderer import Renderer
from constants import State


class Movable(pg.sprite.Sprite):
    instances = list()

    def __init__(self, position, sprite="no_sprite.png", dimensions=cfg.FIGHTER_SIZE):
        pg.sprite.Sprite.__init__(self)
        self.renderer = Renderer(self)
        self.state = State.idle
        self.state_timer = 0
        self.image_name = sprite
        self.image = UI.prepare_image(sprite, dimensions)
        self.rect = self.image.get_rect(bottomleft=position)

        self.movement_vector = 0
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.direction = 1

    def set_dash_timer(self, time):
        self.dash_timer = time

    def set_dashing(self):
        if self.dash_cooldown == 0:
            self.dash_timer = cfg.DASH_TIME
            self.dash_cooldown = cfg.DASH_TIME + cfg.DASH_COOLDOWN

    def manage_dashing(self):
        self.dash_timer_tick()
        if self.state == State.dashing:
            self.movement_vector *= cfg.DASH_MULTIPLIER

    def manage_ducking(self):
        if self.state == State.ducking:
            self.movement_vector /= 2

    def manage_idling(self):
        if self.movement_vector == 0 and self.state != State.ducking:
            self.set_state(State.idle)

    def dash_timer_tick(self):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.dash_timer > 0:
            self.dash_timer -= 1
        elif self.state == State.dashing:
            self.set_state(State.idle)

    def update(self, *args, **kwargs) -> None:
        if self.state_timer > 0:
            self.state_timer -= 1
        self.movement_vector = cfg.MOVE_SPEED * self.direction
        self.manage_idling()
        self.manage_ducking()
        self.manage_dashing()
        self.rect.x += self.movement_vector
        self.image = self.renderer.render_frame()
        self.rect = self.image.get_rect(bottomleft=(self.rect.x, cfg.FLOOR))

    def set_state(self, state):
        if self.state != state and self.state_timer == 0:
            if state == State.jabbing:
                self.state_timer = cfg.JAB_DURATION
            self.state = state
            self.renderer.update()


class Living(Movable):
    def __init__(self, *args, hp=cfg.FULL_HP, **kwargs):
        super(Living, self).__init__(*args, **kwargs)
        self.health = hp
        self.stamina = 100
        self.balance = 100
        self.damage_modifier = 1
        self.statuses = set()
        Movable.instances.append(self)

    def update(self, *args, **kwargs) -> None:
        super(Living, self).update(self)
