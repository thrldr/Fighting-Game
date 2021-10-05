from enum import Enum
import constants as c


class State:
    states = {}

    class Type(Enum):
        movement = 1
        attack = 2
        misc = 3
        dashing = 4

    def __init__(self, key, duration, state_type, modifier):
        self.key = key
        self.duration = duration
        self.type = state_type
        self.modifier = modifier
        State.states.update({key: self})

    @staticmethod
    def initialize_states():
        State("idle", 0, State.Type.movement, 0)
        State("walking", 15, State.Type.movement, 1)
        State("walking_back", 18, State.Type.movement, -1)
        State("ducking", c.MIN_DUCKING_DURATION, State.Type.movement, 0)
        State("dashing", c.DASH_DURATION, State.Type.dashing, c.DASH_MULTIPLIER)
        State("dashing_back", c.DASH_DURATION, State.Type.dashing, c.DASH_MULTIPLIER * -1)
        State("jabbing", c.JAB_DURATION, State.Type.attack, 1)
        State("staggered", c.STAGGER_DURATION, State.Type.movement, 0)

