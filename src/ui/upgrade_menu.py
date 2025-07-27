import pygame
from constants import *
from utils.image_loader import load_image

class UpgradeMenu:
    def __init__(self, screen, player, logger, current_score):
        self.screen = screen
        self.player = player
        self.logger = logger
        self.current_score = current_score
        self.font = pygame.font.Font(None, 60) # Fuente más grande para el título
        self.option_font = pygame.font.Font(None, 40) # Fuente para las opciones
        self.desc_font = pygame.font.Font(None, 30) # Fuente para descripciones
        self.options = list(UPGRADES.keys())
        self.selected_option_index = 0
        self.message = "" # Mensaje para el jugador
        self.message_timer = 0 # Temporizador para el mensaje
        self.message_duration = 2000 # Duración del mensaje en ms

        # Cargar imagen de fondo
        self.background_image = load_image("assets/images/fondos/game_background_1_dark.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def show(self):
        menu_options = self.options + ["continue_game"]
        
        # Asegurarse de que la opción seleccionada sea válida si la lista de opciones cambia
        if self.selected_option_index >= len(menu_options):
            self.selected_option_index = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option_index = (self.selected_option_index - 1) % len(menu_options)
                        self.message = "" # Limpiar mensaje al cambiar de opción
                    elif event.key == pygame.K_DOWN:
                        self.selected_option_index = (self.selected_option_index + 1) % len(menu_options)
                        self.message = "" # Limpiar mensaje al cambiar de opción
                    elif event.key == pygame.K_RETURN:
                        if menu_options[self.selected_option_index] == "continue_game":
                            running = False # Sale del menú de mejoras
                        else:
                            selected_upgrade_key = menu_options[self.selected_option_index]
                            upgrade_info = UPGRADES[selected_upgrade_key]
                            cost = upgrade_info["cost"]

                            if self.current_score >= cost:
                                self.current_score -= cost
                                self.apply_upgrade(selected_upgrade_key)
                                self.message = f"Mejora comprada: {upgrade_info['name']}!"
                                self.message_timer = pygame.time.get_ticks()
                                self.logger.log_event(f"Mejora comprada: {upgrade_info['name']}. Puntuación restante: {self.current_score}")
                            else:
                                self.message = f"Puntos insuficientes para {upgrade_info['name']}."
                                self.message_timer = pygame.time.get_ticks()
                                self.logger.log_event(f"Puntuación insuficiente para {upgrade_info['name']}.")

            self.screen.blit(self.background_image, (0, 0)) # Dibujar el fondo

            # Título
            title_text = self.font.render("Menú de Mejoras", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(title_text, title_rect)

            # Puntuación actual
            score_text = self.option_font.render(f"Puntuación: {self.current_score}", True, YELLOW)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(score_text, score_rect)

            y_offset = 200
            for i, option_key in enumerate(menu_options):
                is_selected = (i == self.selected_option_index)
                
                if option_key == "continue_game":
                    option_name = "Continuar Juego"
                    option_cost_str = ""
                    option_description = "Regresar al juego."
                    can_afford = True # Siempre se puede continuar
                else:
                    upgrade_info = UPGRADES[option_key]
                    option_name = upgrade_info["name"]
                    cost = upgrade_info["cost"]
                    option_cost_str = f" (Costo: {cost})"
                    option_description = upgrade_info["description"]
                    can_afford = (self.current_score >= cost)

                # Determinar color de la opción
                color = WHITE
                if is_selected:
                    color = YELLOW if can_afford else RED # Amarillo si seleccionada y asequible, rojo si no
                elif not can_afford and option_key != "continue_game":
                    color = (100, 100, 100) # Gris si no es asequible y no seleccionada

                # Dibujar rectángulo de la opción
                option_rect_width = 800 # Aumentar ancho
                option_rect_height = 100 # Aumentar alto
                option_rect = pygame.Rect(0, 0, option_rect_width, option_rect_height)
                option_rect.center = (SCREEN_WIDTH // 2, y_offset)
                
                pygame.draw.rect(self.screen, (50, 50, 50), option_rect, border_radius=10) # Fondo del rectángulo
                if is_selected:
                    pygame.draw.rect(self.screen, YELLOW, option_rect, 3, border_radius=10) # Borde si seleccionada

                # Texto de la opción
                option_text_surface = self.option_font.render(f"{option_name}{option_cost_str}", True, color)
                option_text_rect = option_text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset - 20))
                self.screen.blit(option_text_surface, option_text_rect)

                # Descripción de la opción
                desc_text_surface = self.desc_font.render(option_description, True, WHITE)
                desc_text_rect = desc_text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 25))
                self.screen.blit(desc_text_surface, desc_text_rect)

                y_offset += 120 # Aumentar espaciado
            
            # Mostrar mensaje temporal
            if self.message and (pygame.time.get_ticks() - self.message_timer < self.message_duration):
                message_surface = self.font.render(self.message, True, YELLOW)
                message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
                self.screen.blit(message_surface, message_rect)

            pygame.display.flip()

    def apply_upgrade(self, upgrade_key):
        upgrade_info = UPGRADES[upgrade_key]
        effect = upgrade_info["effect"]

        if "speed" in effect:
            self.player.speed += effect["speed"]
        if "lives" in effect:
            self.player.lives += effect["lives"]
        if "shot_delay" in effect:
            self.player.shot_delay += effect["shot_delay"]
            # Asegurarse de que shot_delay no sea negativo
            if self.player.shot_delay < 0.05:
                self.player.shot_delay = 0.05
        if "projectile_speed" in effect:
            self.player.projectile_speed += effect["projectile_speed"]
        if "attack_type" in effect:
            self.player.set_attack_type(effect["attack_type"])