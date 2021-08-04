import cfg
import game_logic
from enemy_generator import Enemy_generator
import entities
import player_input as pinput
import pygame as pg


def game_over(main_surf):
    for entity in entities.Living.entities_list:
        entity.die()
    impact_font = pg.font.SysFont('Impact', 90)
    small_impact_font = pg.font.SysFont('Arial', 30)
    game_over_text = impact_font.render("GAME OVER", 1, "RED", cfg.TEXT_BG_COLOR)
    restart_text = small_impact_font.render("press Enter to restart", 1, "BLACK")
    pos = game_over_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 100))
    restart_pos = restart_text.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 + 200))
    main_surf.fill(cfg.BG_COLOR)
    main_surf.blit(game_over_text, pos)
    main_surf.blit(restart_text, restart_pos)

    image_surface = pg.image.load("dead.bmp")
    image_rect = image_surface.get_rect(center=(cfg.DISPLAY_X // 2, cfg.DISPLAY_Y // 2 - 150))
    main_surf.blit(image_surface, image_rect)
    pg.display.update()


def start_game(main_surf, clock):
    print("hi")
    player = entities.Player(cfg.DISPLAY_X / 2 - 25, cfg.FLOOR)
    i = 0
    continue_loop = True
    while continue_loop:

        pinput.input_placeholder(player)

        # enemy creation
        i += 1
        if len(entities.Enemy.entities_list) < 10 and i % 20 == 0:
            Enemy_generator.generate()

        # render stuff
        main_surf.fill("BLACK")
        for entity in entities.Living.entities_list:
            entity.surface.fill(entity.color)
            main_surf.blit(entity.surface, (entity.x_pos, entity.y_pos))

        for bullet in entities.Projectile.existing_projectiles:
            bullet.surface.fill("WHITE")
            main_surf.blit(bullet.surface, (bullet.x_pos, bullet.y_pos))
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
        for enemy in entities.Enemy.existing_enemies:
            enemy.rush(player)
            if player.is_collided(enemy):
                continue_loop = False

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

        clock.tick(cfg.FPS)

    continue_loop = True
    while continue_loop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                continue_loop = False
            if event.type == pg.QUIT:
                exit()
        game_over(main_surf)
        clock.tick(cfg.FPS)
