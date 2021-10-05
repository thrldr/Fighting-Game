import constants as cfg
import pygame as pg
import UI
from renderer import Renderer
from states import State


class Movable(pg.sprite.Sprite):
    instances = list()

    def __init__(self, position, sprite="no_sprite.png", dimensions=cfg.FIGHTER_SIZE, direction=1):
        pg.sprite.Sprite.__init__(self)
        Movable.instances.append(self)
        self.renderer = Renderer(self)

        self.state = State.states["idle"]
        self.state_timer = 0
        self.cooldown = {"dashing": 0, "dashing_back": 0}

        self.image_name = sprite
        self.image = UI.prepare_image(sprite, dimensions)
        self.rect = self.image.get_rect(bottomleft=position)

        self.head_rect = pg.Rect(self.rect.x + 35, self.rect.y + 30, 55, 55)

        self.hand_collision_rect = pg.Rect(self.rect.x + self.rect.width / 2 * direction + 110 * direction, self.rect.y + 50, *cfg.HAND_COLLISION_SIZE)

        self.movement_vector = 0
        self.direction = direction

    def manage_received_attacks(self):
        for entity in Movable.instances:
            if self.head_rect.colliderect(entity.hand_collision_rect) and entity != self \
                    and entity.state == State.states['jabbing'] and entity.state_timer < 7:
                self.set_state(State.states['staggered'])

    def state_timer_tick(self):
        if self.state_timer > 0:
            self.state_timer -= 1
        for key in self.cooldown.keys():
            if self.cooldown[key] > 0:
                self.cooldown[key] -= 1

    def handle_state(self):
        self.state_timer_tick()
        if self.state.type is State.Type.dashing:
            self.cooldown["dashing"] = cfg.DASH_COOlDOWN
            self.cooldown["dashing_back"] = cfg.DASH_COOlDOWN
        if self.state.type is State.Type.movement or self.state.type is State.Type.dashing:
            self.movement_vector *= self.state.modifier
        else:
            self.movement_vector = 0

    def get_rect_by_direction(self):
        if self.direction == 1:
            self.rect = self.image.get_rect(bottomleft=(self.rect.x, cfg.FLOOR))
        else:
            self.rect = self.image.get_rect(bottomright=(self.rect.x + self.rect.width, cfg.FLOOR))

    def update(self, *args, **kwargs) -> None:
        self.movement_vector = cfg.MOVE_SPEED * self.direction
        self.handle_state()
        self.manage_received_attacks()

        self.rect.move_ip(self.movement_vector, 0)
        self.image = self.renderer.render_frame()

        self.get_rect_by_direction()
        self.hand_collision_rect.move_ip(self.movement_vector, 0)

        self.hand_collision_rect.x = self.rect.x + self.rect.width / 2  # !!!

        if self.state_timer == 0:
            self.set_state(State.states["idle"])

    def turn_around(self):
        self.direction *= -1
        self.renderer.load_fighter_animations()

    def set_state(self, state):
        if self.state != state and self.cooldown.get(state.key, 0) == 0:
            self.state_timer = state.duration
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

    def update(self, *args, **kwargs) -> None:
        super(Living, self).update(self)
