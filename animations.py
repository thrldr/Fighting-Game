import pygame as pg
import constants as cfg


class Animation:
    def __init__(self, name, path, frame_durations, flip=False, size=cfg.FIGHTER_SIZE):
        self.name = name
        self.path = path
        self.frames = {}
        self.frame_data = self.load_animation_frames_by_durations(path, frame_durations, size, flip)

    def load_animation_frames_by_durations(self, folder_path, durations, size, flip):
        frame_data = []
        n = 0
        for frame_duration in durations:
            frame_id = str(n)
            try:
                image_path = folder_path + '/' + frame_id + '.bmp'
                self.frames[frame_id] = pg.image.load(image_path).convert_alpha()
            except FileNotFoundError:
                image_path = folder_path + '/' + frame_id + '.png'
                self.frames[frame_id] = pg.image.load(image_path).convert_alpha()
            self.frames[frame_id] = pg.transform.scale(self.frames[frame_id], size)
            if flip:
                self.frames[frame_id] = pg.transform.flip(self.frames[frame_id], True, False)

            for i in range(frame_duration):
                frame_data.append(frame_id)
            n += 1
        return frame_data
