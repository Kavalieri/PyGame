import pygame
import sys
from game_loop import GameLoop
from ui.menu import Menu
from ui.pause_menu import PauseMenu
from managers.logger import Logger
from managers.save_manager import SaveManager
from constants import *

def main():
    # Inicialización de Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Usar las constantes actualizadas
    pygame.display.set_caption('Juego Modularizado')
    clock = pygame.time.Clock()
    running = True

    # Crear instancia del logger
    logger = Logger()

    # Crear instancia del save manager
    save_manager = SaveManager(logger=logger)

    # Crear instancia del bucle del juego, pasando el logger
    game = GameLoop(screen, logger)

    # Crear instancia del menú
    menu = Menu(screen, save_manager, logger, game)

    game_started = False
    while not game_started:
        action = menu.show_main_menu()

        if action == "new_game":
            slot_number = menu.show_new_game_save_slot_selection()
            if slot_number is not None:
                selected_character = menu.show_character_selection_menu()
                if selected_character:
                    game.player.set_character_stats(selected_character)
                    # Guardar el estado inicial del juego en el slot seleccionado
                    initial_game_state = game.get_game_state()
                    save_manager.save_game(slot_number, initial_game_state)
                    game_started = True
            else:
                # Si el usuario cancela la selección de slot, vuelve al menú principal
                continue
        elif action == "load_game":
            loaded_state = menu.show_load_menu()
            if loaded_state:
                game.apply_game_state(loaded_state)
                game_started = True
        elif action == "exit":
            running = False
            game_started = True # Salir del bucle de selección de menú
        elif action == "continue": # Si se guardó el juego, continuar con la partida actual
            game_started = True

    paused = False # Nueva bandera para el estado de pausa
    pause_menu = PauseMenu(screen, logger) # Instancia del menú de pausa

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    paused = not paused # Alternar estado de pausa
            if not paused and event.type == pygame.MOUSEBUTTONDOWN:
                game.player.shoot(event.pos[0], event.pos[1])

        if not paused:
            # Actualizar lógica del juego
            game.update()

            # Dibujar en pantalla
            game.draw()
        else:
            # Si está pausado, mostrar el menú de pausa
            action = pause_menu.show()
            if action == "resume":
                paused = False
            elif action == "main_menu":
                running = False
                game_started = False # Volver al menú principal

        clock.tick(FPS)

        if game.game_over: # Usar la bandera game_over del GameLoop
            running = False

    if game.game_over: # Si el juego terminó por game over
        menu.show_game_over(game.enemies_destroyed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
