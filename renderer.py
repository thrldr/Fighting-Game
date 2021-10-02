import UI
import constants as cfg
from animations import Animation


class Renderer:
    def __init__(self, target):
        self.puppet = target
        self.animations = dict()
        self.frame_number = 0
        self.current_animation = "idle"
        self.load_player_animations()

    def load_animation(self, animation: Animation):
        self.animations[animation.name] = animation

    def load_player_animations(self):
        self.load_animation(Animation("idle", r"resources\sprites\animations\idle", (9, 4, 5, 10, 5, 4)))
        self.load_animation(Animation("ducking", r"resources\sprites\animations\ducking", (10,), cfg.DUCKING_FIGHTER_SIZE))
        self.load_animation(Animation("dashing", r"resources\sprites\animations\dashing", (2, 3, 4, 2, 1, 1)))
        self.load_animation(Animation("jabbing", r"resources\sprites\animations\jabbing", (1, 2, 7, 4, 4)))
        self.load_animation(Animation("walking", r"resources\sprites\animations\walking", (3, 3, 3, 3, 3, 3)))
        self.load_animation(Animation("walking_back", r"resources\sprites\animations\walking_back", (3, 3, 3, 3, 3, 3)))

    def render_frame(self):
        if self.frame_number < len(self.animations[self.current_animation].frame_data):
            self.frame_number += 1
        else:
            self.frame_number = 1

        # print("State: ", self.puppet.state, "; Animation: ", self.current_animation)
        try:
            frame = self.animations[self.current_animation]\
                .frames[self.animations[self.puppet.state.value].frame_data[self.frame_number - 1]]
            return frame
        except KeyError:
            return UI.prepare_image("no_sprite.png", cfg.FIGHTER_SIZE)

    def update(self):
        self.frame_number = 0
        self.current_animation = self.puppet.state.value

