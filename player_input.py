import pygame as pg
import game_states
import cfg


class Controller:
    def __init__(self, controllable, processor):
        self.puppet = controllable
        self.processor = processor
        self.can_double_tap = False

    def check_double_tap(self):
        pass

    def handle_events(self):
        if self.puppet is None:
            raise AttributeError

        # single keys
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.processor.pause_game()
                if event.key == pg.K_x:
                    self.puppet.kill()
                if event.key == pg.K_RIGHT:
                    self.handle_double_tap()
                    self.puppet.direction = 1
                if event.key == pg.K_LEFT:
                    self.handle_double_tap()
                    self.puppet.direction = -1

        # pressed keys
        pressed_keys = pg.key.get_pressed()
        self.puppet.movement_vector = Controller.get_distance_from_keys_pressed(pressed_keys)
        self.puppet.is_crouching = Controller.is_crouching(pressed_keys)

    def handle_double_tap(self):
        if self.puppet.dash_timer > 0 and self.can_double_tap:
            self.puppet.set_dashing()
            self.can_double_tap = False
        else:
            self.can_double_tap = True
            self.puppet.set_dash_timer(cfg.DOUBLE_TAP_DURATION)

    @staticmethod
    def is_crouching(pressed_keys):
        if pressed_keys[pg.K_DOWN]:
            return True
        else:
            return False

    @staticmethod
    def get_distance_from_keys_pressed(pressed_keys):
        speed = cfg.MOVE_SPEED
        if pressed_keys[pg.K_LEFT]:
            return -speed

        elif pressed_keys[pg.K_RIGHT]:
            return speed
        else:
            return 0
