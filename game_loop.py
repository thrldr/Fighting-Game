import cfg
from os import chdir
import game_logic
from enemy_generator import Enemy_generator
import entities
import player_input as pinput
import pygame as pg
pg.init()


# initializing board
chdir(r"C:/Users/thrldr/Desktop/res")
pg.display.set_caption("scaffolding")
pg.display.set_icon(pg.image.load("icon.bmp"))
clock = pg.time.Clock()

main_surf = pg.display.set_mode((cfg.DISPLAY_X, cfg.DISPLAY_Y))

player = entities.Player(cfg.DISPLAY_X / 2 - 25, cfg.FLOOR)

# Game Loop
i = 0
continue_loop = True
while continue_loop:
    pinput.input_placeholder(player)

    # enemy creation
    if i > 30000:
        i = 0
    else:
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
        if event.type == pg.QUIT:
            exit()
    game_logic.game_over(main_surf)
    clock.tick(cfg.FPS)