import pygame
import sys
from src.managers.enemy_generator import EnemyGenerator
from src.ui.hud import HUD
from src.entities.player import Player
from src.entities.enemy import Enemy
import random
from src.core.constants import *
from src.managers.sound_manager import SoundManager
from src.entities.powerups import PowerUp


class GameLoop:
    def __init__(self, screen, logger):
        self.logger = logger
        self.logger.log_debug("Bucle del juego inicializado")
        self.screen = screen
        self.enemies = []
        self.sound_manager = SoundManager(logger=self.logger)
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - PLAYER_SIZE * 2, logger=logger, sound_manager=self.sound_manager)
        self.player.logger = logger  # Añadir logger al jugador si es necesario
        self.hud = HUD(screen)
        self.enemies_destroyed = 0
        self.ground_line = SCREEN_HEIGHT  # Línea del suelo
        self.enemy_generator = EnemyGenerator(logger=self.logger)
        self.powerups = [] # Lista para almacenar los power-ups
        self.stars = []
        for _ in range(100): # Generar 100 estrellas
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            self.stars.append([x, y, size])
        self.sound_manager.play_music("sounds/background_music.mp3") # Asumiendo que tienes un archivo de música

    def update(self):
        self.player.update()
        
        # Generar enemigos si es necesario
        new_enemies = self.enemy_generator.generate_enemies(self.enemies_destroyed)
        self.enemies.extend(new_enemies)

        for enemy in self.enemies:
            enemy.move()
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_off_screen(self.ground_line)]

        for projectile in self.player.projectiles:
            projectile.move()
        self.player.projectiles = [p for p in self.player.projectiles if p.y > 0] # Eliminar proyectiles fuera de pantalla

        # Detectar colisiones entre proyectiles y enemigos
        for projectile in self.player.projectiles[:]: # Usar una copia para poder modificar la lista
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
                    self.player.projectiles.remove(projectile)
                    break

        # Actualizar y dibujar power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            if self.player.collision_box.colliderect(powerup.rect):
                self.player.activate_powerup(powerup.type)
                self.powerups.remove(powerup)
            elif powerup.y > SCREEN_HEIGHT:
                self.powerups.remove(powerup)


        for enemy in self.enemies[:]: # Usar una copia para poder modificar la lista
            if self.player.x < enemy.x + enemy.size and self.player.x + self.player.size > enemy.x and self.player.y < enemy.y + enemy.size and self.player.y + self.player.size > enemy.y:
                self.enemies.remove(enemy)
                self.player.lose_life()
            elif enemy.is_off_screen(self.ground_line):
                self.enemies.remove(enemy)  # Eliminar enemigo que impactó el suelo
        self.logger.log_debug(f"Actualizando juego: enemigos={len(self.enemies)}, proyectiles={len(self.player.projectiles)}, powerups={len(self.powerups)}")

    def draw(self):
        self.screen.fill(BLACK)
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, (star[0], star[1]), star[2])
            star[1] += star[2] # Mover la estrella hacia abajo
            if star[1] > SCREEN_HEIGHT: # Si la estrella sale de la pantalla, resetearla arriba
                star[1] = 0
                star[0] = random.randint(0, SCREEN_WIDTH)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        self.player.draw(self.screen)  # Dibujar al jugador en la pantalla
        self.hud.draw(self.player.lives, self.enemies_destroyed)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            target_x, target_y = pygame.mouse.get_pos()
            self.player.shoot(target_x, target_y)
            self.logger.log_debug(f"Disparo realizado hacia x={target_x}, y={target_y}")
        elif event.type == pygame.QUIT:
            self.logger.log_event("Juego terminado por el usuario")
            pygame.quit()
            sys.exit()
