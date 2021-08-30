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