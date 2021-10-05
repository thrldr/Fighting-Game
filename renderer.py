import UI
import constants as cfg
from animations import Animation
import pygame as pg


class Renderer:
    def __init__(self, target):
        self.puppet = target
        self.animations = dict()
        self.frame_number = 0
        self.current_animation = "idle"

    def load_animations(self, *animations):
        for animation in animations:
            self.animations[animation.name] = animation

    def load_player_animations(self):
        self.load_animations(
            Animation("idle", r"resources\sprites\animations\idle", (9, 4, 5, 10, 5, 4)),
            Animation("ducking", r"resources\sprites\animations\ducking", (10,), size=cfg.DUCKING_FIGHTER_SIZE),
            Animation("dashing", r"resources\sprites\animations\dashing", (2, 3, 4, 2, 1, 1)),
            Animation("dashing_back", r"resources\sprites\animations\dashing", (2, 3, 4, 2, 1, 1)),
            Animation("jabbing", r"resources\sprites\animations\jabbing", (2, 2, 7, 4, 3),
                      size=(cfg.FIGHTER_SIZE[1], cfg.FIGHTER_SIZE[1])),
            Animation("staggered", r"resources\sprites\animations\staggered", (2, 2, 4, 3, 3)),
            Animation("walking", r"resources\sprites\animations\walking", (3, 3, 3, 2, 2, 2)),
            Animation("walking_back", r"resources\sprites\animations\walking_back", (2, 2, 2, 3, 4, 5))
        )

    def load_fighter_animations(self):
        if self.puppet.direction == 1:
            to_flip = False
        else:
            to_flip = True
        self.load_animations(
            Animation("idle", r"resources\sprites\animations\idle", (9, 4, 5, 10, 5, 4), flip=to_flip),
            Animation("ducking", r"resources\sprites\animations\ducking", (10,), size=cfg.DUCKING_FIGHTER_SIZE,
                      flip=to_flip),
            Animation("dashing", r"resources\sprites\animations\dashing", (2, 3, 4, 2, 1, 1), flip=to_flip),
            Animation("dashing_back", r"resources\sprites\animations\dashing", (2, 3, 4, 2, 1, 1)),
            Animation("jabbing", r"resources\sprites\animations\jabbing", (1, 2, 7, 4, 4), flip=to_flip,
                      size=(cfg.FIGHTER_SIZE[1], cfg.FIGHTER_SIZE[1])),
            Animation("staggered", r"resources\sprites\animations\staggered", (2, 3, 4, 3, 2), flip=to_flip),
            Animation("walking", r"resources\sprites\animations\walking", (3, 3, 3, 3, 3, 3), flip=to_flip),
            Animation("walking_back", r"resources\sprites\animations\walking_back", (4, 4, 4, 4, 4, 4), flip=to_flip)
        )

    def render_frame(self):
        if self.frame_number < len(self.animations[self.current_animation].frame_data):
            self.frame_number += 1
        else:
            self.frame_number = 1

        try:
            frame = self.animations[self.current_animation] \
                .frames[self.animations[self.puppet.state.key].frame_data[self.frame_number - 1]]
            return frame
        except KeyError:
            return UI.prepare_image("no_sprite.png", cfg.FIGHTER_SIZE)

    def update(self):
        self.frame_number = 0
        self.current_animation = self.puppet.state.key
