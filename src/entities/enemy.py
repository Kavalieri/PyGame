#!/usr/bin/env python3
"""
Entidad Enemigo para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Lógica, animaciones y barra de vida de los enemigos del juego.
"""
import pygame
import random
import time
from constants import *
from entities.projectile import Projectile
from utils.image_loader import load_image, load_animation_frames
from utils.advanced_logger import get_logger

class Enemy:
    def __init__(self, x, y, enemy_type, rarity="NORMAL", logger=None):
        self.x = x
        self.y = y
        self.logger = logger or get_logger("PyGame")
        self.enemy_type = enemy_type
        self.rarity = rarity

        # Obtener estadísticas base del tipo de enemigo
        stats = ENEMY_TYPES.get(enemy_type, ENEMY_TYPES["ZOMBIE_MALE"]) # Default a ZOMBIE_MALE
        self.size = stats["size"]
        self.base_speed = stats["speed"]
        self.base_health = stats["health"]
        self.can_shoot = stats.get("can_shoot", False)
        self.shoot_delay = stats.get("shoot_delay", 2.0)
        self.last_shot_time = time.time()
        self.movement_pattern = stats["movement_pattern"]

        # Aplicar multiplicadores de rareza
        rarity_stats = ENEMY_RARITIES.get(rarity, ENEMY_RARITIES["NORMAL"])
        self.speed = self.base_speed * rarity_stats["speed_multiplier"]
        self.health = int(self.base_health * rarity_stats["health_multiplier"])
        self.score_value = int(10 * rarity_stats["score_multiplier"]) # Valor de puntuación base 10

        self.collision_box = pygame.Rect(self.x, self.y, self.size, self.size)

        # Para movimiento zigzag
        self.zigzag_amplitude = 50 # Qué tan lejos se mueve horizontalmente
        self.zigzag_speed_multiplier = 0.05 # Velocidad del zigzag
        self.zigzag_direction = 1 # 1 para derecha, -1 para izquierda

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

        # Inicializar barra de vida y marco según rareza (usando Health_03)
        self.health_frame_image = pygame.image.load("assets/ui/Health_03.png")
        if rarity == "NORMAL":
            self.health_bar_image = pygame.image.load("assets/ui/Health_03_Bar01.png")
        elif rarity == "RARE":
            self.health_bar_image = pygame.image.load("assets/ui/Health_03_Bar02.png")
        elif rarity in ("EPIC", "ELITE", "LEGENDARY"):
            self.health_bar_image = pygame.image.load("assets/ui/Health_03_Bar03.png")
        else:
            self.health_bar_image = pygame.image.load("assets/ui/Health_03_Bar01.png")

        # Asignar un frame inicial como imagen base
        self.image = self.animation_frames["idle"][0] if self.animation_frames["idle"] else None

        self.logger.log_debug(f"Enemigo {enemy_type} ({rarity}) creado en posición x={self.x}, y={self.y}, tamaño={self.size}, velocidad={self.speed}, salud={self.health}, can_shoot={self.can_shoot}", "enemy")
        self.logger.log_debug(f"Health frame image: {self.health_frame_image}, Health bar image: {self.health_bar_image}", "enemy")

    def move(self):
        """Mueve el enemigo según su patrón de movimiento."""
        if self.movement_pattern == "straight":
            self.y += self.speed
        elif self.movement_pattern == "zigzag":
            # Movimiento zigzag horizontal mientras baja
            self.y += self.speed
            self.x += self.zigzag_direction * self.speed * self.zigzag_speed_multiplier
            
            # Cambiar dirección cuando llega a los bordes
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
                self.zigzag_direction *= -1

        # Actualizar caja de colisión
        self.collision_box.topleft = (self.x, self.y)

    def update(self):
        """Actualiza el estado del enemigo."""
        self.move()
        
        # Actualizar animación
        current_time = time.time()
        if current_time - self.last_frame_update > self.animation_speed:
            if self.current_animation in self.animation_frames and self.animation_frames[self.current_animation]:
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.current_animation])
                self.image = self.animation_frames[self.current_animation][self.current_frame]
            self.last_frame_update = current_time

    def shoot(self, target_x, target_y):
        """Dispara un proyectil hacia el objetivo."""
        if not self.can_shoot:
            return None
            
        current_time = time.time()
        if current_time - self.last_shot_time > self.shoot_delay:
            projectile = Projectile(self.x + self.size // 2, self.y + self.size, 
                                    target_x, target_y, size=10, speed=3, 
                                    image_path="assets/objects/proyectiles/aranazo.png", 
                                    piercing=False, logger=self.logger)
            self.last_shot_time = current_time
            self.logger.log_debug(f"Enemigo {self.enemy_type} dispara proyectil hacia ({target_x}, {target_y})", "enemy")
            return projectile
        return None

    def draw(self, screen):
        """Dibuja el enemigo y su barra de vida."""
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
            screen.blit(scaled_image, (self.x, self.y))
        else:
            # Fallback si no hay imagen
            pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

        # Dibujar barra de vida
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Dibuja la barra de vida del enemigo."""
        bar_width = 50
        bar_height = 8
        bar_x = self.x + (self.size - bar_width) // 2
        bar_y = self.y - 15

        # Dibujar marco de la barra de vida
        screen.blit(self.health_frame_image, (bar_x, bar_y))

        # Calcular el ancho de la barra de vida basado en la salud actual
        max_health = self.base_health * ENEMY_RARITIES.get(self.rarity, ENEMY_RARITIES["NORMAL"])["health_multiplier"]
        health_ratio = max(0, self.health / max_health)
        current_bar_width = int(bar_width * health_ratio)

        if current_bar_width > 0:
            # Crear una superficie para la barra de vida
            health_surface = pygame.Surface((current_bar_width, bar_height))
            health_surface.set_colorkey((0, 0, 0))  # Hacer transparente el fondo negro
            
            # Usar subsurface para obtener solo la parte necesaria de la imagen de la barra
            bar_rect = pygame.Rect(0, 0, current_bar_width, bar_height)
            health_bar_subsurface = self.health_bar_image.subsurface(bar_rect)
            health_surface.blit(health_bar_subsurface, (0, 0))
            
            # Dibujar la barra de vida
            screen.blit(health_surface, (bar_x, bar_y))

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def take_damage(self, damage):
        """Reduce la salud del enemigo."""
        self.health -= damage
        self.logger.log_debug(f"Enemigo {self.enemy_type} recibe {damage} de daño. Salud restante: {self.health}", "enemy")
        
        if self.health <= 0:
            self.logger.log_event(f"Enemigo {self.enemy_type} ({self.rarity}) eliminado", "enemy")
            return True
        return False

    def on_defeat(self):
        # Mostrar puntos sumados
        font = pygame.font.Font(None, 24)
        points_text = font.render(f"+{self.score_value}", True, (0, 255, 0))
        screen = pygame.display.get_surface()
        screen.blit(points_text, (self.x + self.size // 2, self.y - 20))