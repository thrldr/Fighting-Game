import pygame as pg
import constants as cfg
from constants import State


class Controller:
    def __init__(self, controllable, processor):
        self.puppet = controllable
        self.processor = processor
        self.key_buffer = None

    def check_double_tap(self):
        pass

    def handle_events(self):
        if self.puppet is None:
            raise AttributeError("Controller has no puppet")

        # tapped keys
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.processor.pause_game()
                if event.key == pg.K_x:
                    self.puppet.set_state(State.jabbing)
                if event.key == pg.K_q:
                    self.puppet.kill()

                if event.key == pg.K_RIGHT:
                    self.handle_double_tap(pg.K_RIGHT)
                if event.key == pg.K_LEFT:
                    self.handle_double_tap(pg.K_LEFT)

        # pressed keys
        if not self.puppet.state == State.dashing:
            pressed_keys = pg.key.get_pressed()
            self.puppet.direction = Controller.get_direction_from_pressed_keys(pressed_keys)
            if pressed_keys[pg.K_RIGHT]:
                self.puppet.set_state(State.walking)
            elif pressed_keys[pg.K_LEFT]:
                self.puppet.set_state(State.walking_back)
            else:
                self.puppet.set_state(State.idle)
            if pressed_keys[pg.K_DOWN]:
                self.puppet.set_state(State.ducking)

    def handle_double_tap(self, key):
        if self.puppet.dash_timer > 0 and self.key_buffer == key:
            self.puppet.set_dashing()
            self.puppet.direction = Controller.get_direction_from_tapped_key(key)
            self.puppet.set_state(State.dashing)
            self.key_buffer = None
        else:
            self.key_buffer = key
            if not self.puppet.state == State.dashing:
                self.puppet.set_dash_timer(cfg.DOUBLE_TAP_DURATION)

    @staticmethod
    def get_direction_from_tapped_key(key):
        if key == pg.K_LEFT:
            return -1
        elif key == pg.K_RIGHT:
            return 1
        else:
            return 0

    @staticmethod
    def get_direction_from_pressed_keys(pressed_keys):
        if pressed_keys[pg.K_LEFT]:
            return -1
        elif pressed_keys[pg.K_RIGHT]:
            return 1
        else:
            return 0
