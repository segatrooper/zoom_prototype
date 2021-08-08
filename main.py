import game, pygame

if __name__ == '__main__':
    main_game = game.Game((1920, 1080))
    clock = pygame.time.Clock()
    deltaTime = 0
    while True:
        main_game.game_loop(deltaTime)
        deltaTime = clock.tick(30)

