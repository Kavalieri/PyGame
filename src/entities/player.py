import pygame
from src.entities.projectile import Projectile
import sys
import time
from src.core.constants import *

class Player:
    def __init__(self, x, y, logger=None, sound_manager=None):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.projectiles = []
        self.lives = PLAYER_LIVES
        self.logger = logger
        self.sound_manager = sound_manager
        self.collision_box = pygame.Rect(self.x, self.y, self.size, self.size)

        # Power-up related attributes
        self.is_fast_shooting = False
        self.fast_shot_timer = 0
        self.fast_shot_duration = 5 # seconds
        self.has_shield = False
        self.shield_timer = 0
        self.shield_duration = 10 # seconds
        self.last_shot_time = 0
        self.shot_delay = 0.5 # seconds

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        # Limitar el movimiento a la pantalla
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.collision_box.topleft = (self.x, self.y)

        # Update power-up timers
        if self.is_fast_shooting and time.time() - self.fast_shot_timer > self.fast_shot_duration:
            self.is_fast_shooting = False
            self.shot_delay = 0.5 # Reset to normal
            if self.logger:
                self.logger.log_event("Power-up de disparo rápido terminado.")

        if self.has_shield and time.time() - self.shield_timer > self.shield_duration:
            self.has_shield = False
            if self.logger:
                self.logger.log_event("Power-up de escudo terminado.")

    def shoot(self, target_x, target_y):
        current_time = time.time()
        if current_time - self.last_shot_time > self.shot_delay:
            projectile = Projectile(self.x + self.size // 2, self.y, target_x, target_y, logger=self.logger)
            self.projectiles.append(projectile)
            if self.logger:
                self.logger.log_debug(f"Jugador disparó proyectil hacia x={target_x}, y={target_y}")
            if self.sound_manager:
                self.sound_manager.play_sound("shoot")
            self.last_shot_time = current_time

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.size, self.size))
        if self.has_shield:
            pygame.draw.circle(screen, BLUE, (int(self.x + self.size / 2), int(self.y + self.size / 2)), self.size, 3) # Dibujar escudo
        for projectile in self.projectiles:
            projectile.draw(screen)

    def lose_life(self, amount=1):
        """Reduce las vidas del jugador."""
        if self.has_shield:
            self.has_shield = False
            if self.logger:
                self.logger.log_event("Escudo absorbió el daño.")
            return

        self.lives -= amount
        if self.logger:
            self.logger.log_event(f"Jugador pierde vida. Vidas restantes: {self.lives}")
        if self.lives <= 0:
            if self.logger:
                self.logger.log_event("Game Over")
            print("Game Over")
            pygame.quit()
            sys.exit()

    def activate_powerup(self, powerup_type):
        if powerup_type == "health":
            self.lives += 1
            if self.logger:
                self.logger.log_event("Power-up de salud recogido!")
        elif powerup_type == "fast_shot":
            self.is_fast_shooting = True
            self.fast_shot_timer = time.time()
            self.shot_delay = 0.1 # Faster shooting
            if self.logger:
                self.logger.log_event("Power-up de disparo rápido activado!")
        elif powerup_type == "shield":
            self.has_shield = True
            self.shield_timer = time.time()
            if self.logger:
                self.logger.log_event("Power-up de escudo activado!")
