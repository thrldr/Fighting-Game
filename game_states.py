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
    for entity in entities.Living.entities_list:
        if isinstance(entity, entities.Player):
            player = entity
    if not processor.can_continue:
        clear_board()
        player = entities.Player(cfg.DISPLAY_X * 0.25, cfg.FLOOR, *cfg.FIGHTER_SIZE)
        enemy = entities.Enemy(cfg.DISPLAY_X * 0.75 - 100, cfg.FLOOR, *cfg.FIGHTER_SIZE)

    h = 0
    h_e = 0
    processor.set_state("defeat")
    hitting = False
    e_hitting = False
    enemy_moves = False
    enemy_vector = 0

    while processor.continue_loop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                processor.pause_game()
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                hitting = True
            if event.type == pg.QUIT:
                exit()

        # render stuff
        processor.main_surface.fill("BLACK")
        for entity in entities.Living.entities_list:
            entity.surface.fill(entity.color)
            processor.main_surface.blit(entity.surface, (entity.x_pos, entity.y_pos))

        # movement logic
        # player movement

        #
        #   TODO: IMPLEMENT SIMPLER CURVES
        #

        if hitting:
            hand = pg.Surface((curves.hitting_curve(h), 20))
            hand.fill("GREEN")
            if pg.Rect((player.x_pos + player.width, cfg.FLOOR + 50, curves.hitting_curve(h), 20)).colliderect(pg.Rect((enemy.x_pos, enemy.y_pos, *cfg.FIGHTER_SIZE))):
                enemy.HP -= 25
                if enemy.HP <= 0:
                    processor.continue_loop = False
                    processor.set_state("victory")
                h = 15
            processor.main_surface.blit(hand, (player.x_pos + player.width, cfg.FLOOR + 50))
            h += 1
            if h > 14:
                hitting = False
                h = 0

        if random.randint(0, 50) == 10:
            e_hitting = True

        if e_hitting:
            e_hand = pg.Surface((curves.hitting_curve(h_e), 20))
            e_hand.fill("RED")
            if pg.Rect((enemy.x_pos - curves.hitting_curve(h_e), cfg.FLOOR + 40, curves.hitting_curve(h_e), 20)).colliderect(pg.Rect((player.x_pos, player.y_pos, *cfg.FIGHTER_SIZE))):
                player.HP -= 25
                if player.HP <= 0:
                    processor.continue_loop = False
                    processor.set_state("defeat")
                h_e = 15
            processor.main_surface.blit(e_hand, (enemy.x_pos - curves.hitting_curve(h_e), cfg.FLOOR + 40))
            h_e += 1
            if h_e > 14:
                e_hitting = False
                h_e = 0

        move_vector = pinput.get_distance_from_keys_pressed()
        player.set_direction(move_vector)

        collision_cause = player.seek_possible_collision(move_vector)
        if collision_cause is None:
            player.x_pos += move_vector
        else:
            player.x_pos += player.get_distance_to(collision_cause)

        if not enemy_moves:
            enemy_movement_time = random.randint(5, 20)
            enemy_vector = random.randint(-1, 1)
            enemy_moves = True
        else:
            if enemy_movement_time > 0:
                enemy_movement_time -= 1
            else:
                enemy_moves = False
            if enemy.x_pos + enemy.width + cfg.MOVE_SPEED > cfg.DISPLAY_X:
                enemy_vector *= -1
            enemy.x_pos += enemy_vector * cfg.MOVE_SPEED

        processor.clock.tick(cfg.FPS)

        UI.draw_hp(processor.main_surface, player.HP, enemy.HP)
        pg.display.flip()
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
