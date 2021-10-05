import constants as cfg
import entities
import player_input as pinput
import pygame as pg
import UI
from states import State
from menus import Menu_Renderer as Menu


def start_game_cycle(processor):

    if not processor.can_continue:
        State.initialize_states()
        player = entities.Living(cfg.PLAYER_STARTING_POS)
        player.renderer.load_fighter_animations()
        enemy = entities.Living(cfg.ENEMY_STARTING_POS, direction=-1)
        enemy.renderer.load_fighter_animations()
        fighters = pg.sprite.Group()
        fighters.add(player)
        fighters.add(enemy)

    controller = pinput.Controller(player, processor)

    background_shape = pg.surface.Surface((cfg.DISPLAY_X, cfg.FLOOR // 1.6))

    background_shape.fill("YELLOW")
    processor.main_surface.fill("BLACK")
    pg.display.update()

    collision_shape = pg.surface.Surface((55, 55))
    collision_hand = pg.surface.Surface(cfg.HAND_COLLISION_SIZE)
    test = pg.surface.Surface((500, 500))

    while processor.continue_loop:

        processor.main_surface.fill("BLACK")
        processor.main_surface.blit(background_shape, (0, cfg.FLOOR // 2.2))
        UI.draw_text(processor.main_surface, enemy.state_timer, enemy.state.key)    # debug text

        controller.handle_events()
        fighters.update()
        fighters.draw(processor.main_surface)

        collision_shape.fill("RED")
        test.fill("BLUE")
        collision_hand.fill(pg.Color(255, 0, 0))
        collision_hand.set_alpha(150)

        # processor.main_surface.blit(collision_shape, enemy.head_rect)
        processor.main_surface.blit(collision_hand, player.hand_collision_rect)

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
