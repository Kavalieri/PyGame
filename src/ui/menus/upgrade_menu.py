import pygame
from constants import UPGRADES, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
from utils.image_loader import load_image
from ui.menus.base_menu import BaseMenu

class UpgradeMenu(BaseMenu):
    def __init__(self, screen, player, logger, current_score):
        self.player = player
        self.current_score = current_score
        self.points_spent = 0
        self.upgrade_levels = {k: player.get_upgrade_level(k) for k in UPGRADES}

        options_data = []
        for upgrade_key, upgrade_info in UPGRADES.items():
            level = self.upgrade_levels.get(upgrade_key, 0)
            options_data.append({
                "text": f"{upgrade_info['name']} (Nivel: {level}) - {upgrade_info['description']} (Costo: {upgrade_info['cost']})",
                "action": upgrade_key
            })
        options_data.append({"text": "Continuar Juego", "action": "continue_game"})
        options_data.insert(0, {"text": "Resetear mejoras", "action": "reset_upgrades"})

        super().__init__(screen, logger, title_text="Menú de Mejoras", options=options_data,
                         background_image_path="assets/images/fondos/game_background_1_dark.png",
                         button_images={
                             'normal': "assets/images/ui/Buttons/Blue/Blank 1.png",
                             'hover': "assets/images/ui/Buttons/Blue/Blank 2.png"
                         })

        self.background_image = load_image("assets/images/fondos/parque.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.message = "" # Mensaje para el jugador
        self.message_timer = 0 # Temporizador para el mensaje
        self.message_duration = 2000 # Duración del mensaje en ms

        self.current_page = 0  # Página actual para la navegación por páginas

    def show(self):
        self.logger.log_debug("[UpgradeMenu] Entrando en show()")
        print("[UpgradeMenu] Entrando en show()")
        while True:
            self._draw()
            action = self._handle_input()
            print(f"[UpgradeMenu] Acción recibida: {action}")
            self.logger.log_debug(f"[UpgradeMenu] Acción recibida: {action}")
            if action == "toggle_pause":
                print("[UpgradeMenu] Ignorando toggle_pause (ESC) en menú de mejoras")
                self.logger.log_debug("[UpgradeMenu] Ignorando toggle_pause (ESC) en menú de mejoras")
                continue
            elif action == "continue_game":
                print("[UpgradeMenu] Seleccionado continuar juego. Saliendo de show().")
                self.logger.log_debug("[UpgradeMenu] Seleccionado continuar juego. Saliendo de show().")
                return
            elif action == "reset_upgrades":
                self._reset_upgrades()
                continue
            elif action:
                selected_upgrade_key = action
                print(f"[UpgradeMenu] Intentando aplicar mejora: {selected_upgrade_key}")
                self.logger.log_debug(f"[UpgradeMenu] Intentando aplicar mejora: {selected_upgrade_key}")
                if selected_upgrade_key not in UPGRADES:
                    print(f"[UpgradeMenu] Clave de mejora desconocida: {selected_upgrade_key}")
                    self.logger.log_error(f"[UpgradeMenu] Clave de mejora desconocida: {selected_upgrade_key}")
                    self.message = "Error: Mejora desconocida."
                    self.message_timer = pygame.time.get_ticks()
                    continue

                upgrade_info = UPGRADES[selected_upgrade_key]
                cost = upgrade_info["cost"]

                if self.current_score >= cost:
                    self.current_score -= cost
                    self.points_spent += cost
                    self.apply_upgrade(selected_upgrade_key)
                    self.upgrade_levels[selected_upgrade_key] = self.upgrade_levels.get(selected_upgrade_key, 0) + 1
                    print(f"[UpgradeMenu] Mejora comprada: {upgrade_info['name']}! Puntuación restante: {self.current_score}")
                    self.logger.log_event(f"[UpgradeMenu] Mejora comprada: {upgrade_info['name']}. Puntuación restante: {self.current_score}")
                    self.message = f"Mejora comprada: {upgrade_info['name']}!"
                    self.message_timer = pygame.time.get_ticks()
                    # Actualizar texto de la opción
                    for opt in self.options:
                        if opt["action"] == selected_upgrade_key:
                            opt["text"] = f"{upgrade_info['name']} (Nivel: {self.upgrade_levels[selected_upgrade_key]}) - {upgrade_info['description']} (Costo: {upgrade_info['cost']})"
                else:
                    print(f"[UpgradeMenu] Puntos insuficientes para {upgrade_info['name']}.")
                    self.logger.log_event(f"[UpgradeMenu] Puntuación insuficiente para {upgrade_info['name']}.")
                    self.message = f"Puntos insuficientes para {upgrade_info['name']}."
                    self.message_timer = pygame.time.get_ticks()

            if self.message:
                self._draw_message()

    def _draw(self):
        # HUD de puntos y control
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(BLACK)

        # Título reposicionado
        font_title = pygame.font.Font(None, 60)
        title_surface = font_title.render("Menú de Mejoras", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_surface, title_rect)

        # Puntos disponibles y gastados
        font_info = pygame.font.Font(None, 36)
        puntos_disp = font_info.render(f"Puntos disponibles: {self.current_score}", True, (0,255,0))
        puntos_gast = font_info.render(f"Puntos gastados: {self.points_spent}", True, (255,200,0))
        self.screen.blit(puntos_disp, (40, 140))
        self.screen.blit(puntos_gast, (40, 180))

        # Llamar al renderizado de botones y opciones del menú base
        super()._draw()

    def _draw_message(self):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.message, True, (255, 255, 255)) # Blanco
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def _reset_upgrades(self):
        # Resetear mejoras y devolver puntos gastados
        self.logger.log_event("[UpgradeMenu] Reseteando mejoras y devolviendo puntos gastados.")
        print("[UpgradeMenu] Reseteando mejoras y devolviendo puntos gastados.")
        self.current_score += self.points_spent
        self.points_spent = 0
        for k in self.upgrade_levels:
            self.upgrade_levels[k] = 0
        if hasattr(self.player, "upgrades"):
            self.player.upgrades = {}
        self.message = "Mejoras reseteadas. Puntos devueltos."
        self.message_timer = pygame.time.get_ticks()
        # Actualizar texto de las opciones
        for opt in self.options:
            if opt["action"] in UPGRADES:
                info = UPGRADES[opt["action"]]
                opt["text"] = f"{info['name']} (Nivel: 0) - {info['description']} (Costo: {info['cost']})"

    def apply_upgrade(self, upgrade_key):
        """Aplica el efecto de la mejora seleccionada al jugador y actualiza upgrades."""
        upgrade_info = UPGRADES[upgrade_key]
        effect = upgrade_info["effect"]
        if not hasattr(self.player, "upgrades"):
            self.player.upgrades = {}
        if upgrade_key not in self.player.upgrades:
            self.player.upgrades[upgrade_key] = {"level": 0}
        self.player.upgrades[upgrade_key]["level"] += 1
        # Aplicar efectos
        for attr, value in effect.items():
            if attr == "speed":
                self.player.speed += value
            elif attr == "lives":
                self.player.lives += value
            elif attr == "shot_delay":
                self.player.shot_delay = max(0.05, self.player.shot_delay + value) # No bajar de 0.05
            elif attr == "projectile_speed":
                self.player.projectile_speed += value
            elif attr == "attack_type":
                self.player.set_attack_type(value)
        self.logger.log_event(f"[UpgradeMenu] Efecto de mejora aplicado: {upgrade_info['name']} ({effect})")
