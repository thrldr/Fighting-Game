from pygame.surface import Surface

import cfg
import entities
import player_input as pinput
import pygame as pg
import UI
import random
from menus import Menu_Renderer as Menu
from enemy_spawn import clear_board


def start_game_cycle(processor):

    if not processor.can_continue:
        player = entities.Living((cfg.DISPLAY_X // 4.5, cfg.FLOOR), sprite="right_stance.png")
        player.image.set_colorkey("WHITE")
        player_group = pg.sprite.Group()
        player_group.add(player)
        controller = pinput.Controller(player, processor)

    background_shape = pg.surface.Surface((cfg.DISPLAY_X, cfg.FLOOR // 1.5))

    background_shape.fill("YELLOW")
    processor.main_surface.fill("BLACK")
    pg.display.update()

    while processor.continue_loop:

        processor.main_surface.fill("BLACK")
        processor.main_surface.blit(background_shape, (0, cfg.FLOOR // 2.2))
        UI.draw_text(processor.main_surface, player.is_dashing, player.dash_timer)

        controller.handle_events()
        player_group.update()
        player_group.draw(processor.main_surface)

        processor.clock.tick(cfg.FPS)
        pg.display.update()
    processor.continue_loop = True


def start_main_menu_cycle(processor):
    if processor.can_continue:
        main_menu = Menu("Continue", "New Game", "Exit")
    else:
        main_menu = Menu("New Game", "Exit")

    while processor.continue_loop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            main_menu.read_controls(event, processor)
        main_menu.show_on(processor.main_surface)
        UI.draw_fighting_image_on(processor.main_surface)
        pg.display.update()
        processor.clock.tick(cfg.FPS)
    processor.set_state("gameplay")
    processor.continue_loop = True


def start_game_over_cycle(processor, win):
    while processor.continue_loop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                processor.continue_loop = False
            if event.type == pg.QUIT:
                exit()

        if win:
            UI.draw_victory_screen_on(processor.main_surface)
        else:
            UI.draw_defeat_screen_on(processor.main_surface)
        pg.display.update()
        processor.clock.tick(cfg.FPS)
    processor.set_state("main_menu")
    processor.continue_loop = True
