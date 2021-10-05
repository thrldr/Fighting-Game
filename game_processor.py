import game_states as gc
import pygame as pg
import constants as cfg
from enum import Enum


# to do: switch game processor states implementation from plain strings to enum
class Game_Processor:
    class State(Enum):
        idle = 0
        main_menu = 1
        victory = 2
        defeat = 3
        gameplay = 4

    def __init__(self, state="idle"):
        Game_Processor.check_if_valid_state(state)
        self.continue_loop = True
        self.can_continue = False
        self.state = state
        self.clock = pg.time.Clock()
        self.main_surface = pg.display.set_mode((cfg.DISPLAY_X, cfg.DISPLAY_Y))
        self.win = False

    @staticmethod
    def check_if_valid_state(state):
        if state not in cfg.states:
            raise ValueError

    def pause_game(self):
        self.continue_loop = False
        self.can_continue = True
        self.set_state("main_menu")

    def get_state(self):
        return self.state

    def handle_state(self):
        if self.state == 'main_menu':
            gc.start_main_menu_cycle(self)
        elif self.state == 'victory':
            gc.start_game_over_cycle(self, win=True)
        elif self.state == 'defeat':
            gc.start_game_over_cycle(self, win=False)
        elif self.state == 'gameplay':
            gc.start_game_cycle(self)

    def set_state(self, state, win=False):
        self.win = win
        Game_Processor.check_if_valid_state(state)
        self.state = state
