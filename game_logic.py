import entities
import cfg
import pygame as pg
import game_cycle as gc


class Bar:
    def __init__(self, name, status="inactive"):
        self.name = name
        self.status = status

    def is_active(self):
        if self.status == "active":
            return True
        else:
            return False

    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "inactive"

    def get_name(self):
        return self.name


class Menus:
    def __init__(self, *args):
        self.bars = list()
        self.font = pg.font.SysFont('Impact', 40)
        for arg in args:
            self.bars.append(Bar(arg))
        self.bars[0].activate()

    def show_on(self, surface):
        surface.fill(cfg.BG_COLOR)
        for i, bar in enumerate(self.bars):
            if bar.is_active():
                background_color = cfg.TEXT_BG_COLOR
            else:
                background_color = None
            rendered_bar = self.font.render(bar.get_name(), 1, cfg.TEXT_COLOR, background_color)
            surface.blit(rendered_bar, rendered_bar.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 50 + i * 100)))

    def read_controls(self, event, main_surf, clock):
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
            for i, bar in enumerate(self.bars):
                if bar.is_active():
                    bar.deactivate()
                    if i + 1 == len(self.bars):
                        self.bars[0].activate()
                    else:
                        self.bars[i + 1].activate()
                    break

        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
            for i, bar in enumerate(self.bars):
                if bar.is_active():
                    bar.deactivate()
                    if i - 1 < 0:
                        self.bars[-1].activate()
                    else:
                        self.bars[i - 1].activate()
                    break

        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            for bar in self.bars:
                if bar.is_active():
                    if bar.get_name() == "Exit":
                        exit()
                    elif bar.get_name() == "New Game":
                        gc.start_game(main_surf, clock)


