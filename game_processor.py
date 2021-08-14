import time

import pygame as pg
import cfg
from enemy_generator import Enemy_generator
import entities
import player_input as pinput
import UI
from menus import Menu_Renderer as Menu


def clear_board():
    while len(entities.Projectile.existing_projectiles) > 0 :
        for bullet in entities.Projectile.existing_projectiles:
            bullet.die()
    while len(entities.Living.entities_list) > 0:
        for entity in entities.Living.entities_list:
            entity.die()


class Game_Processor:
    def __init__(self, state="idle"):
        Game_Processor.check_if_valid_state(state)
        self.continue_loop = True
        self.can_continue = False
        self.state = state
        self.clock = pg.time.Clock()
        self.main_surface = pg.display.set_mode((cfg.DISPLAY_X, cfg.DISPLAY_Y))

    @staticmethod
    def check_if_valid_state(state):
        if state not in cfg.states:
            raise ValueError

    def get_state(self):
        return self.state

    def handle_state(self):
        if self.state == 'main_menu':
            start_main_menu_cycle(self)
        elif self.state == 'game_over':
            start_game_over_cycle(self)
        elif self.state == 'gameplay':
            start_game(self)

    def set_state(self, state):
        Game_Processor.check_if_valid_state(state)
        self.state = state


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


def start_game_over_cycle(processor):
    while processor.continue_loop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                processor.continue_loop = False
            if event.type == pg.QUIT:
                exit()

        UI.draw_game_over_screen_on(processor.main_surface)
        pg.display.update()
        processor.clock.tick(cfg.FPS)
    processor.set_state("main_menu")
    processor.continue_loop = True


def start_game(processor):
    for entity in entities.Living.entities_list:
        if isinstance(entity, entities.Player):
            player = entity
    if not processor.can_continue:
        clear_board()
        player = entities.Player(cfg.DISPLAY_X / 2 - 25, cfg.FLOOR)

    i = 0
    next_state = "game_over"
    while processor.continue_loop:

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                player.shoot()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                processor.continue_loop = False
                processor.can_continue = True
                next_state = "main_menu"
            if event.type == pg.QUIT:
                exit()

        # enemy creation
        i += 1
        if len(entities.Enemy.entities_list) < 10 and i > 100 and i % 30 == 0:
            Enemy_generator.generate()

        # render stuff
        processor.main_surface.fill("BLACK")
        for entity in entities.Living.entities_list:
            entity.surface.fill(entity.color)
            processor.main_surface.blit(entity.surface, (entity.x_pos, entity.y_pos))

        for bullet in entities.Projectile.existing_projectiles:
            bullet.surface.fill("WHITE")
            processor.main_surface.blit(bullet.surface, (bullet.x_pos, bullet.y_pos))
        pg.display.flip()

        # movement logic
        # player movement
        move_vector = pinput.get_distance_from_keys_pressed()
        player.set_direction(move_vector)

        collision_cause = player.seek_possible_collision(move_vector)
        if collision_cause is None:
            player.x_pos += move_vector
        else:
            player.x_pos += player.get_distance_to(collision_cause)

        # enemy movement
        if not player.is_dead:
            for enemy in entities.Enemy.existing_enemies:
                enemy.rush(player)
                if player.is_collided(enemy):
                    player.is_dead = True
                    player.die()
                    processor.can_continue = False
                    processor.continue_loop = False
                    clear_board()
                    clear_board()

        # bullets logic
        for projectile in entities.Projectile.existing_projectiles:
            # checking if there are victims and killing them
            for target in entities.Enemy.existing_enemies:
                if projectile.is_collided(target):
                    projectile.die()
                    target.die()

            move_vector = cfg.PROJECTILE_SPEED * cfg.DIRECTIONS[projectile.direction]
            collision_cause = projectile.seek_possible_collision(move_vector)
            if collision_cause is None:
                projectile.x_pos += move_vector
                if projectile.out_of_display():
                    del projectile
            else:
                projectile.x_pos += projectile.get_distance_to(collision_cause)

        processor.clock.tick(cfg.FPS)
    processor.set_state(next_state)
    processor.continue_loop = True



