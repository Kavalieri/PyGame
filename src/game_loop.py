import pygame
import sys
import time
import random
from managers.enemy_generator import EnemyGenerator
from ui.hud import HUD
from entities.player import Player
from entities.enemy import Enemy
from constants import *
from managers.sound_manager import SoundManager
from entities.powerups import PowerUp
from ui.upgrade_menu import UpgradeMenu # Importar el menú de mejoras
from utils.image_loader import load_image


class GameLoop:
    def __init__(self, screen, logger):
        self.logger = logger
        self.logger.log_debug("Bucle del juego inicializado")
        self.screen = screen
        self.enemies = []
        self.enemy_projectiles = [] # Lista para almacenar los proyectiles de los enemigos
        self.sound_manager = SoundManager(logger=self.logger)
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - PLAYER_SIZE * 2, logger=logger, sound_manager=self.sound_manager)
        self.player.logger = logger  # Añadir logger al jugador si es necesario
        self.hud = HUD(screen)
        self.enemies_destroyed = 0
        self.ground_line = SCREEN_HEIGHT  # Línea del suelo
        self.enemy_generator = EnemyGenerator(logger=self.logger)
        self.powerups = [] # Lista para almacenar los power-ups
        
        # Cargar fondo de pantalla
        self.background_image = load_image(random.choice(BACKGROUND_IMAGES))
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Atributos de nivel
        self.current_level = 1
        self.level_start_time = time.time()
        self.level_duration = LEVELS[self.current_level]["duration"]
        self.game_over = False

    def reset_level(self):
        self.enemies = []
        self.enemy_projectiles = []
        self.powerups = []
        self.level_start_time = time.time()
        self.level_duration = LEVELS[self.current_level]["duration"]
        self.logger.log_event(f"Nivel {self.current_level} reiniciado.")

    def update(self):
        if self.game_over:
            return

        self.player.update()
        
        # Lógica de niveles
        elapsed_level_time = time.time() - self.level_start_time
        if elapsed_level_time > self.level_duration:
            self.current_level += 1
            if self.current_level > len(LEVELS):
                self.logger.log_event("¡Juego completado!")
                self.game_over = True # Marcar juego como completado
                return
            else:
                self.logger.log_event(f"Avanzando al Nivel {self.current_level}")
                # Mostrar menú de mejoras al final del nivel
                upgrade_menu = UpgradeMenu(self.screen, self.player, self.logger, self.enemies_destroyed) # enemies_destroyed como puntuación
                upgrade_menu.show()
                self.reset_level()

        # Generar enemigos si es necesario
        new_enemies = self.enemy_generator.generate_enemies(self.enemies_destroyed)
        self.enemies.extend(new_enemies)

        for enemy in self.enemies:
            enemy.move()
            # Enemigos disparan al jugador
            if enemy.can_shoot:
                projectile = enemy.shoot(self.player.x + self.player.size // 2, self.player.y + self.player.size // 2)
                if projectile:
                    self.enemy_projectiles.append(projectile)

        self.enemies = [enemy for enemy in self.enemies if not enemy.is_off_screen(self.ground_line)]

        for projectile in self.player.projectiles:
            projectile.move()
        self.player.projectiles = [p for p in self.player.projectiles if p.y > 0] # Eliminar proyectiles fuera de pantalla

        # Actualizar proyectiles enemigos
        for projectile in self.enemy_projectiles:
            projectile.move()
        self.enemy_projectiles = [p for p in self.enemy_projectiles if p.y < SCREEN_HEIGHT] # Eliminar proyectiles enemigos fuera de pantalla

        # Detectar colisiones entre proyectiles del jugador y enemigos
        for projectile in self.player.projectiles[:]: # Usar una copia para poder modificar la lista
            projectile_hit = False
            for enemy in self.enemies[:]: # Usar una copia para poder modificar la lista
                if enemy.collision_box.colliderect(pygame.Rect(projectile.x, projectile.y, projectile.size, projectile.size)):
                    if enemy.take_damage(1): # El proyectil hace 1 de daño
                        self.enemies.remove(enemy)
                        self.enemies_destroyed += 1
                        self.sound_manager.play_sound("explosion") # Reproducir sonido de explosión
                        # Posibilidad de soltar power-up
                        if random.random() < 0.2: # 20% de probabilidad
                            powerup_type = random.choice(["health", "fast_shot", "shield"])
                            self.powerups.append(PowerUp(enemy.x, enemy.y, powerup_type, logger=self.logger))
                    if not projectile.piercing:
                        projectile_hit = True
                        break
            if projectile_hit:
                self.player.projectiles.remove(projectile)

        # Detectar colisiones entre proyectiles enemigos y el jugador
        for projectile in self.enemy_projectiles[:]:
            if self.player.collision_box.colliderect(pygame.Rect(projectile.x, projectile.y, projectile.size, projectile.size)):
                self.player.lose_life(1) # El proyectil enemigo hace 1 de daño
                self.enemy_projectiles.remove(projectile)

        # Actualizar y dibujar power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            if self.player.collision_box.colliderect(powerup.rect):
                self.player.activate_powerup(powerup.type)
                self.powerups.remove(powerup)
            elif powerup.y > SCREEN_HEIGHT:
                self.powerups.remove(powerup)


        for enemy in self.enemies[:]: # Usar una copia para poder modificar la lista
            if self.player.collision_box.colliderect(enemy.collision_box):
                self.enemies.remove(enemy)
                self.player.lose_life()
            elif enemy.is_off_screen(self.ground_line):
                self.enemies.remove(enemy)  # Eliminar enemigo que impactó el suelo
        self.logger.log_debug(f"Actualizando juego: enemigos={len(self.enemies)}, proyectiles={len(self.player.projectiles)}, powerups={len(self.powerups)}")

        if self.player.lives <= 0:
            self.game_over = True

    def draw(self):
        if self.game_over:
            return

        self.screen.blit(self.background_image, (0, 0)) # Dibujar el fondo
        # Las estrellas ya no son necesarias con un fondo
        # for star in self.stars:
        #     pygame.draw.circle(self.screen, WHITE, (star[0], star[1]), star[2])
        #     star[1] += star[2] # Mover la estrella hacia abajo
        #     if star[1] > SCREEN_HEIGHT: # Si la estrella sale de la pantalla, resetearla arriba
        #         star[1] = 0
        #         star[0] = random.randint(0, SCREEN_WIDTH)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        for projectile in self.enemy_projectiles: # Dibujar proyectiles enemigos
            projectile.draw(self.screen)
        self.player.draw(self.screen)  # Dibujar al jugador en la pantalla
        active_powerups = {}
        if self.player.is_fast_shooting:
            active_powerups["Disparo Rápido"] = self.player.fast_shot_duration - (time.time() - self.player.fast_shot_timer)
        if self.player.has_shield:
            active_powerups["Escudo"] = self.player.shield_duration - (time.time() - self.player.shield_timer)
        self.hud.draw(self.player.lives, self.enemies_destroyed, self.current_level, max(0, self.level_duration - (time.time() - self.level_start_time)), active_powerups)
        pygame.display.flip()

    def handle_event(self, event):
        if self.game_over:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            target_x, target_y = pygame.mouse.get_pos()
            self.player.shoot(target_x, target_y)
            self.logger.log_debug(f"Disparo realizado hacia x={target_x}, y={target_y}")
        elif event.type == pygame.QUIT:
            self.logger.log_event("Juego terminado por el usuario")
            pygame.quit()
            sys.exit()

    def get_game_state(self):
        player_state = {
            "x": self.player.x,
            "y": self.player.y,
            "lives": self.player.lives,
            "is_fast_shooting": self.player.is_fast_shooting,
            "fast_shot_timer": self.player.fast_shot_timer,
            "has_shield": self.player.has_shield,
            "shield_timer": self.player.shield_timer,
            "last_shot_time": self.player.last_shot_time,
            "shot_delay": self.player.shot_delay,
            "character_type": self.player.character_type, # Guardar el tipo de personaje
            "projectile_speed": self.player.projectile_speed, # Guardar la velocidad del proyectil
        }
        enemies_state = []
        for enemy in self.enemies:
            enemies_state.append({
                "x": enemy.x,
                "y": enemy.y,
                "size": enemy.size,
                "speed": enemy.speed,
                "image_path": "assets/images/objects/Skeleton.png", # Guardar la ruta de la imagen del enemigo
                "health": enemy.health,
            })
        powerups_state = []
        for powerup in self.powerups:
            powerups_state.append({
                "x": powerup.x,
                "y": powerup.y,
                "type": powerup.type,
                "size": powerup.size,
                "color": powerup.color,
                "speed": powerup.speed,
            })
        return {
            "player": player_state,
            "enemies": enemies_state,
            "powerups": powerups_state,
            "enemies_destroyed": self.enemies_destroyed,
            "current_level": self.current_level,
            "level_start_time": self.level_start_time,
        }

    def apply_game_state(self, game_state):
        self.player.x = game_state["player"]["x"]
        self.player.y = game_state["player"]["y"]
        self.player.lives = game_state["player"]["lives"]
        self.player.is_fast_shooting = game_state["player"]["is_fast_shooting"]
        self.player.fast_shot_timer = game_state["player"]["fast_shot_timer"]
        self.player.has_shield = game_state["player"]["has_shield"]
        self.player.shield_timer = game_state["player"]["shield_timer"]
        self.player.last_shot_time = game_state["player"]["last_shot_time"]
        self.player.shot_delay = game_state["player"]["shot_delay"]
        self.player.set_character_stats(game_state["player"]["character_type"]) # Aplicar stats del personaje
        self.player.projectile_speed = game_state["player"]["projectile_speed"] # Cargar la velocidad del proyectil

        self.enemies = []
        for enemy_data in game_state["enemies"]:
            enemy = Enemy(enemy_data["x"], enemy_data["y"], enemy_data["size"], enemy_data["speed"], image_path=enemy_data["image_path"], health=enemy_data["health"], logger=self.logger)
            self.enemies.append(enemy)

        self.powerups = []
        for powerup_data in game_state["powerups"]:
            powerup = PowerUp(powerup_data["x"], powerup_data["y"], powerup_data["type"], logger=self.logger)
            self.powerups.append(powerup)
        
        self.enemies_destroyed = game_state["enemies_destroyed"]
        self.current_level = game_state["current_level"]
        self.level_start_time = game_state["level_start_time"]
        self.level_duration = LEVELS[self.current_level]["duration"]
        self.logger.log_event("Estado del juego aplicado desde el guardado.")