import pygame
from constants import *
from managers.save_manager import SaveManager
from managers.logger import Logger
from utils.image_loader import load_image, load_animation_frames
import os

class Menu:
    def __init__(self, screen, save_manager: SaveManager, logger: Logger, game_loop):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 40) # Ajustado para más texto
        self.character_name_font = pygame.font.Font(None, 60) # Fuente para el nombre del personaje
        self.save_manager = save_manager
        self.logger = logger
        self.game_loop = game_loop

    def show(self, message):
        # This method will now primarily call show_main_menu
        self.show_main_menu()

    def wait_for_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    return

    def show_main_menu(self):
        options = ["Nueva Partida", "Cargar Partida", "Guardar Juego", "Salir"]
        selected_option = 0

        while True:
            self.screen.fill(BLACK)
            title_text = self.font.render("Juego Modularizado", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(title_text, title_rect)

            for i, option in enumerate(options):
                color = WHITE
                if i == selected_option:
                    color = RED
                option_text = self.small_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 60))
                self.screen.blit(option_text, option_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            return "new_game"
                        elif selected_option == 1:
                            return "load_game"
                        elif selected_option == 2:
                            self.show_save_menu()
                            return "continue" # Vuelve al juego después de guardar
                        elif selected_option == 3:
                            return "exit"

    def show_save_menu(self):
        slots_status = self.save_manager.get_save_slots_status()
        options = []
        for i in range(1, 4):
            status = "(Ocupado)" if slots_status[i] else "(Vacío)"
            options.append(f"Slot {i} {status}")
        options.append("Volver")

        selected_slot = 0

        while True:
            self.screen.fill(BLACK)
            title_text = self.font.render("Guardar Juego", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(title_text, title_rect)

            for i, option in enumerate(options):
                color = WHITE
                if i == selected_slot:
                    color = RED
                option_text = self.small_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 60))
                self.screen.blit(option_text, option_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_slot = (selected_slot - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_slot = (selected_slot + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_slot == len(options) - 1: # Volver
                            return
                        else:
                            slot_number = selected_slot + 1
                            self.logger.log_event(f"Intentando guardar en el slot {slot_number}")
                            game_state = self.game_loop.get_game_state()
                            self.save_manager.save_game(slot_number, game_state)
                            return

    def show_load_menu(self):
        slots_status = self.save_manager.get_save_slots_status()
        options = []
        for i in range(1, 4):
            status = "(Ocupado)" if slots_status[i] else "(Vacío)"
            options.append(f"Slot {i} {status}")
        options.append("Volver")

        selected_slot = 0

        while True:
            self.screen.fill(BLACK)
            title_text = self.font.render("Cargar Juego", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(title_text, title_rect)

            for i, option in enumerate(options):
                color = WHITE
                if i == selected_slot:
                    color = RED
                option_text = self.small_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 60))
                self.screen.blit(option_text, option_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_slot = (selected_slot - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_slot = (selected_slot + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_slot == len(options) - 1: # Volver
                            return None # No se cargó nada
                        else:
                            slot_number = selected_slot + 1
                            self.logger.log_event(f"Intentando cargar del slot {slot_number}")
                            loaded_state = self.save_manager.load_game(slot_number)
                            return loaded_state # Devuelve el estado cargado

    def show_new_game_save_slot_selection(self):
        slots_status = self.save_manager.get_save_slots_status()
        options = []
        for i in range(1, 4):
            status = "(Ocupado)" if slots_status[i] else "(Vacío)"
            options.append(f"Slot {i} {status}")
        options.append("Volver")

        selected_slot = 0

        while True:
            self.screen.fill(BLACK)
            title_text = self.font.render("Selecciona Slot para Nueva Partida", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(title_text, title_rect)

            for i, option in enumerate(options):
                color = WHITE
                if i == selected_slot:
                    color = RED
                option_text = self.small_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 60))
                self.screen.blit(option_text, option_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_slot = (selected_slot - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_slot = (selected_slot + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_slot == len(options) - 1: # Volver
                            return None # No se seleccionó slot
                        else:
                            slot_number = selected_slot + 1
                            # Aquí podrías añadir una confirmación si el slot está ocupado
                            return slot_number

    def show_character_selection_menu(self):
        characters = list(CHARACTER_STATS.keys())
        selected_character_index = 0

        # Cargar las imágenes de los personajes para el menú
        character_images = {}
        for char_name, stats in CHARACTER_STATS.items():
            # Cargar el primer frame de la animación 'Idle' como representación
            image_folder = stats["image_folder"]
            try:
                # Usar load_animation_frames para obtener el primer frame de Idle
                idle_frames = load_animation_frames(image_folder, "Idle", stats["idle_frames"])
                if idle_frames:
                    image = idle_frames[0]
                    character_images[char_name] = pygame.transform.scale(image, (PLAYER_SIZE * 2, PLAYER_SIZE * 2)) # Escalar para mostrar mejor
                else:
                    self.logger.log_error(f"No se encontraron frames para la animación Idle de {char_name}")
                    character_images[char_name] = pygame.Surface((PLAYER_SIZE * 2, PLAYER_SIZE * 2))
                    character_images[char_name].fill(RED) # Placeholder
            except SystemExit:
                self.logger.log_error(f"No se pudo cargar la imagen para {char_name} en {image_folder}")
                character_images[char_name] = pygame.Surface((PLAYER_SIZE * 2, PLAYER_SIZE * 2))
                character_images[char_name].fill(RED) # Placeholder

        while True:
            self.screen.fill(BLACK)
            title_text = self.font.render("Selecciona tu Personaje", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50)) # Ajustar posición del título
            self.screen.blit(title_text, title_rect)

            # Mostrar nombre del personaje seleccionado en grande
            selected_char_name_full = CHARACTER_STATS[characters[selected_character_index]]["name"]
            char_name_surface = self.character_name_font.render(selected_char_name_full, True, YELLOW)
            char_name_rect = char_name_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(char_name_surface, char_name_rect)

            # Mostrar descripción del personaje seleccionado
            selected_char_name = characters[selected_character_index]
            selected_char_stats = CHARACTER_STATS[selected_char_name]
            description_text = self.small_font.render(selected_char_stats["description"], True, WHITE)
            description_rect = description_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(description_text, description_rect)

            # Mostrar imagen del personaje seleccionado
            if selected_char_name in character_images:
                image = character_images[selected_char_name]
                image_rect = image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)) # Posición central
                self.screen.blit(image, image_rect)

            # Mostrar estadísticas del personaje seleccionado
            stats_y_offset = SCREEN_HEIGHT // 2 + 100
            stats_text = [
                f"Velocidad: {selected_char_stats['speed']}",
                f"Vidas: {selected_char_stats['lives']}",
                f"Cadencia de Disparo: {selected_char_stats['shot_delay']}"
            ]
            for i, stat in enumerate(stats_text):
                stat_render = self.small_font.render(stat, True, WHITE)
                stat_rect = stat_render.get_rect(center=(SCREEN_WIDTH // 2, stats_y_offset + i * 40))
                self.screen.blit(stat_render, stat_rect)

            # Dibujar flechas de navegación
            left_arrow = self.small_font.render("< ", True, WHITE)
            right_arrow = self.small_font.render(" >", True, WHITE)
            self.screen.blit(left_arrow, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100))
            self.screen.blit(right_arrow, (SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT - 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_character_index = (selected_character_index - 1) % len(characters)
                    elif event.key == pygame.K_RIGHT:
                        selected_character_index = (selected_character_index + 1) % len(characters)
                    elif event.key == pygame.K_RETURN:
                        return characters[selected_character_index]

    def show_game_over(self, score):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.small_font.render(f"Puntuación: {score}", True, WHITE)
        restart_text = self.small_font.render("Presiona cualquier tecla para salir", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()
        self.wait_for_key()