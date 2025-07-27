import pygame
import random
import time
from constants import *
from entities.projectile import Projectile
from utils.image_loader import load_image, load_animation_frames

class Enemy:
    def __init__(self, x, y, enemy_type, logger=None):
        self.x = x
        self.y = y
        self.logger = logger
        self.enemy_type = enemy_type

        stats = ENEMY_TYPES.get(enemy_type, ENEMY_TYPES["Basic"])
        self.size = stats["size"]
        self.speed = stats["speed"]
        self.health = stats["health"]
        self.can_shoot = stats.get("can_shoot", False)
        self.shoot_delay = stats.get("shoot_delay", 2.0)
        self.last_shot_time = time.time()

        self.collision_box = pygame.Rect(self.x, self.y, self.size, self.size)

        # Animación
        image_folder = stats["image_folder"]
        self.animation_frames = {}
        self.animation_frames["idle"] = load_animation_frames(image_folder, "Idle", stats["idle_frames"])
        self.animation_frames["run"] = load_animation_frames(image_folder, stats.get("run_animation_key", "Run"), stats["run_frames"])
        self.animation_frames["attack"] = load_animation_frames(image_folder, stats.get("attack_animation_key", "Attack"), stats["attack_frames"])
        
        # Usar run si no hay walk para enemigos
        if "walk_frames" in stats:
            self.animation_frames["walk"] = load_animation_frames(image_folder, "Walk", stats["walk_frames"])
        else:
            self.animation_frames["walk"] = self.animation_frames["run"]

        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.1 # Velocidad de cambio de frame
        self.last_frame_update = time.time()

        if not self.animation_frames["idle"]:
            self.logger.log_error(f"No se encontraron frames para la animación Idle de {enemy_type}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(RED) # Placeholder rojo
        else:
            self.image = self.animation_frames["idle"][0] # Establecer el primer frame como imagen inicial

        if self.logger:
            self.logger.log_debug(f"Enemigo {enemy_type} creado en posición x={self.x}, y={self.y}, tamaño={self.size}, velocidad={self.speed}, salud={self.health}, can_shoot={self.can_shoot}")

    def move(self):
        self.y += self.speed
        self.collision_box.topleft = (self.x, self.y)

        # Actualizar animación de movimiento
        if self.speed > 0: # Si se está moviendo hacia abajo
            self.current_animation = "walk" if "walk" in self.animation_frames else "run"
        else:
            self.current_animation = "idle"

        current_time = time.time()
        if current_time - self.last_frame_update > self.animation_speed:
            if self.animation_frames[self.current_animation]: # Añadir esta verificación
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.current_animation])
                self.image = self.animation_frames[self.current_animation][self.current_frame]
            else:
                # Si no hay frames, usar una imagen de placeholder o el último frame conocido
                if self.logger:
                    self.logger.log_warning(f"No hay frames para la animación {self.current_animation} del enemigo {self.enemy_type}. Usando placeholder.")
                self.image = pygame.Surface((self.size, self.size))
                self.image.fill(RED) # Placeholder rojo
            self.last_frame_update = current_time

        if self.logger:
            self.logger.log_debug(f"Enemigo movido a posición x={self.x}, y={self.y}")

    def shoot(self, target_x, target_y):
        current_time = time.time()
        if self.can_shoot and current_time - self.last_shot_time > self.shoot_delay:
            self.current_animation = "attack" # Cambiar a animación de ataque
            self.current_frame = 0 # Reiniciar animación de ataque

            # Usar un sprite para el proyectil del enemigo, si es necesario
            projectile = Projectile(self.x + self.size // 2, self.y + self.size, target_x, target_y, 
                                    color=RED, is_enemy=True, logger=self.logger) # Usar color por defecto o definir sprite
            self.last_shot_time = current_time
            if self.logger:
                self.logger.log_debug(f"Enemigo disparó proyectil hacia x={target_x}, y={target_y}")
            return projectile
        return None

    def draw(self, screen):
        # Dibujar el sprite actual del enemigo
        scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        screen.blit(scaled_image, (self.x, self.y))

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def take_damage(self, damage):
        self.health -= damage
        if self.logger:
            self.logger.log_debug(f"Enemigo en x={self.x}, y={self.y} recibió {damage} de daño. Salud restante: {self.health}")
        return self.health <= 0