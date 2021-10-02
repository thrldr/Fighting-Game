from enum import Enum

DISPLAY_X = 1200
DISPLAY_Y = 900
FPS = 60

FIGHTER_SIZE = (int(DISPLAY_X // 8), int(DISPLAY_Y // 3))
DUCKING_FIGHTER_SIZE = (int(DISPLAY_X // 8), int(DISPLAY_Y // 4))
MOVE_SPEED = DISPLAY_X // 220
FLOOR = DISPLAY_Y - DISPLAY_Y // 3.6

FULL_HP = 100
states = {"idle", "main_menu", "victory", "defeat", "gameplay"}

TEXT_BG_COLOR = "YELLOW"
BG_COLOR = (102, 205, 170)
TEXT_COLOR = "RED"

DASH_TIME = 13
DASH_MULTIPLIER = 2.5
DASH_COOLDOWN = 3
DOUBLE_TAP_DURATION = 14

JAB_DURATION = 14


class State(Enum):
    idle = "idle"
    walking = "walking"
    ducking = "ducking"
    dashing = "dashing"
    walking_back = "walking_back"
    jabbing = "jabbing"
