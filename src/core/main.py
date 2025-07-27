import pygame
import sys
from src.core.game_loop import GameLoop
from src.ui.menu import Menu
from src.managers.logger import Logger
from src.core.constants import *

def main():
    # Inicialización de Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Juego Modularizado')
    clock = pygame.time.Clock()
    running = True

    # Crear instancia del menú y mostrar mensaje inicial
    menu = Menu(screen)
    menu.show("Presiona cualquier tecla para comenzar")
    menu.wait_for_key()

    # Crear instancia del logger
    logger = Logger()

    # Crear instancia del bucle del juego, pasando el logger
    game = GameLoop(screen, logger)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.player.shoot(event.pos[0], event.pos[1])

        # Actualizar lógica del juego
        game.update()

        # Dibujar en pantalla
        game.draw()

        clock.tick(FPS)

        if game.player.lives <= 0:
            running = False

    menu.show_game_over(game.enemies_destroyed)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
