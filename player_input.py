import pygame as pg
import constants as cfg
from states import State


class Controller:
    def __init__(self, controllable, processor):
        self.puppet = controllable
        self.processor = processor
        self.key_buffer = None
        self.__double_tap_timer = 0

    def set_double_tap_timer(self):
        self.__double_tap_timer = cfg.DOUBLE_TAP_DURATION

    def double_tap_timer_tick(self):
        if self.__double_tap_timer > 0:
            self.__double_tap_timer -= 1

    def handle_events(self):
        if self.puppet is None:
            raise AttributeError("Controller has no puppet")

    #   I NEED TO IMPLEMENT A COLLISION SYSTEM OUT OF HITBOX RECTANGLES RESPECTFUL TO BODY PARTS.
    #   ALSO I NEED TO RESHAPE ALL THE ANIMATION FRAMES TO 512*512
    #   ADD A STATE QUE FOR AN ENTITY

        # tapped keys
        self.double_tap_timer_tick()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.processor.pause_game()
                if event.key == pg.K_c:
                    self.puppet.set_state(State.states['staggered'])
                if event.key == pg.K_x:
                    self.puppet.set_state(State.states['jabbing'])
                if event.key == pg.K_z:
                    self.puppet.turn_around()
                if event.key == pg.K_q:
                    self.puppet.kill()

                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    self.handle_double_tap(event.key)

        if not self.puppet.state.type == State.Type.dashing and not self.puppet.state == State.states["jabbing"] \
                or self.puppet.state_timer == 0:

            # pressed keys
            self.handle_pressed_keys()

    def handle_pressed_keys(self):
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[pg.K_RIGHT]:
            if self.puppet.direction == 1:
                self.puppet.set_state(State.states["walking"])
            else:
                self.puppet.set_state(State.states["walking_back"])
        elif pressed_keys[pg.K_LEFT]:
            if self.puppet.direction == 1:
                self.puppet.set_state(State.states["walking_back"])
            else:
                self.puppet.set_state(State.states["walking"])
        elif pressed_keys[pg.K_DOWN]:
            self.puppet.set_state(State.states["ducking"])
        elif self.puppet.state_timer == 0:
            self.puppet.set_state(State.states["idle"])

    def handle_double_tap(self, key):
        if self.__double_tap_timer > 0 and self.key_buffer == key:
            self.key_buffer = None
            if key == pg.K_LEFT:
                self.puppet.set_state(State.states['dashing_back'])
            elif key == pg.K_RIGHT:
                self.puppet.set_state(State.states['dashing'])
        else:
            self.key_buffer = key
            self.set_double_tap_timer()
