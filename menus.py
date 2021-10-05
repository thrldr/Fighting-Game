import constants as cfg
import pygame as pg


class Menu_Bar:
    def __init__(self, name, status="inactive"):
        self.name = name
        self.status = status

    def is_active(self):
        if self.status == "active":
            return True
        elif self.status == "inactive":
            return False
        else:
            raise AttributeError

    def activate(self):
        self.status = "active"

    def deactivate(self):
        self.status = "inactive"

    def get_name(self):
        return self.name


class Menu_Logic:
    def __init__(self, *args, active_bar_position=0):
        self.bars = list()
        self.font = pg.font.SysFont('Impact', 40)
        for arg in args:
            self.bars.append(Menu_Bar(arg))
        self.bars[0].activate()
        self.active_bar_position = active_bar_position

    def get_current_bar(self):
        return self.bars[self.active_bar_position]

    def go_to_next_bar(self):
        self.bars[self.active_bar_position].deactivate()
        if self.active_bar_position + 1 == len(self.bars):
            self.bars[0].activate()
            self.active_bar_position = 0
        else:
            self.bars[self.active_bar_position + 1].activate()
            self.active_bar_position += 1

    def go_to_previous_bar(self):
        self.bars[self.active_bar_position].deactivate()
        if self.active_bar_position - 1 < 0:
            self.bars[len(self.bars) - 1].activate()
            self.active_bar_position = len(self.bars) - 1
        else:
            self.bars[self.active_bar_position - 1].activate()
            self.active_bar_position -= 1


class Menu_Renderer(Menu_Logic):
    def __init__(self, *args, active_bar_position=0):
        Menu_Logic.__init__(self, *args, active_bar_position=0)

    def show_on(self, surface):
        surface.fill(cfg.BG_COLOR)
        for i, bar in enumerate(self.bars):
            if bar.is_active():
                background_color = cfg.TEXT_BG_COLOR
            else:
                background_color = None
            rendered_bar = self.font.render(bar.get_name(), 1, cfg.TEXT_COLOR, background_color)
            surface.blit(rendered_bar, rendered_bar.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 50 + i * 100)))

    def read_controls(self, event, processor):
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
            self.go_to_next_bar()

        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
            self.go_to_previous_bar()

        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            if self.bars[self.active_bar_position].get_name() == "Exit":
                exit()
            elif self.bars[self.active_bar_position].get_name() == "New Game":
                processor.can_continue = False
                processor.continue_loop = False
            elif self.bars[self.active_bar_position].get_name() == "Continue":
                processor.continue_loop = False

