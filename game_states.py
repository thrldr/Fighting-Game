import cfg
import animation_curves as curves
import entities
import player_input as pinput
import pygame as pg
import UI
import random
from menus import Menu_Renderer as Menu
from enemy_spawn import clear_board


def start_game_cycle(processor):
    # creating player
    # for entity in entities.Living.entities_list:
    #     if isinstance(entity, entities.Player):
    #         player = entity
    #     else:
    #         enemy = entity
    # if not processor.can_continue:
    #     clear_board()
    #     player = entities.Player(cfg.DISPLAY_X * 0.25, cfg.FLOOR, *cfg.FIGHTER_SIZE)
    #     enemy = entities.Enemy(cfg.DISPLAY_X * 0.75 - 100, cfg.FLOOR, *cfg.FIGHTER_SIZE)

    player = entities.Movable((cfg.DISPLAY_X // 4.5, cfg.FLOOR), sprite="stance.png")
    player.image.set_colorkey("WHITE")
    player_group = pg.sprite.Group()
    player_group.add(player)

    while processor.continue_loop:
        # CONTROLS
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                player.kill()
                del player
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                processor.pause_game()
            if event.type == pg.QUIT:
                exit()

        player_group.update(pinput.get_distance_from_keys_pressed())
        processor.main_surface.fill("YELLOW")
        player_group.draw(processor.main_surface)

        processor.clock.tick(cfg.FPS)
        pg.display.update(pg.Rect(0, cfg.FLOOR // 2.2, cfg.DISPLAY_X, cfg.FLOOR / 1.5))
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
