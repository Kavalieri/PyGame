#!/usr/bin/env python3
"""
Entidad Jugador para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Lógica, animaciones y gestión de power-ups del jugador principal.
"""
import pygame
from entities.projectile import Projectile
import sys
import time
import math
from constants import *
from utils.image_loader import load_image, load_animation_frames
from utils.advanced_logger import get_logger
import os

class Player:
    def __init__(self, x, y, logger=None, sound_manager=None, character_type="Kava"):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.projectiles = []
        self.logger = logger or get_logger("PyGame")
        self.sound_manager = sound_manager
        self.collision_box = pygame.Rect(self.x, self.y, self.size, self.size)

        # Power-up related attributes
        self.is_fast_shooting = False
        self.fast_shot_timer = 0
        self.fast_shot_duration = 5 # seconds
        self.has_shield = False
        self.shield_timer = 0
        self.shield_duration = 10 # seconds
        self.shield_lives = 0  # Inicializar vidas del escudo
        
        # Animación - Inicializar antes de set_character_stats
        self.animation_frames = {}
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.1 # Velocidad de cambio de frame
        self.last_frame_update = time.time()
        self.facing_left = False # Nueva variable para la dirección

        self.set_character_stats(character_type)
        self.attack_type = "normal" # Default attack type
        self.projectile_speed = PROJECTILE_SPEED # Inicializar con la constante

        if self.logger:
            self.logger.log_event(f"Jugador inicializado en ({self.x},{self.y}) tipo={character_type}", "player")
        print(f"[DEBUG] Jugador inicializado: {self}")

    def set_character_stats(self, character_type):
        stats = CHARACTER_STATS.get(character_type, CHARACTER_STATS["Kava"]) # Cambiado a Kava
        self.speed = stats["speed"]
        self.lives = stats["lives"]
        self.shot_delay = stats["shot_delay"]
        self.original_shot_delay = self.shot_delay # Store original for power-up reset
        self.last_shot_time = 0 # Reset shot timer when character changes
        self.character_type = character_type # Store character type

        # Cargar animaciones usando la función mejorada
        image_folder = stats["image_folder"]
        self.animation_frames["idle"] = load_animation_frames(image_folder, "Idle", stats["idle_frames"])
        self.animation_frames["run"] = load_animation_frames(image_folder, "Run", stats["run_frames"])
        
        # Cargar animación de caminar si existe
        if "walk_frames" in stats:
            self.animation_frames["walk"] = load_animation_frames(image_folder, "Walk", stats["walk_frames"])
        else:
            self.animation_frames["walk"] = self.animation_frames["run"] # Usar run si no hay walk

        self.animation_frames["shoot"] = load_animation_frames(image_folder, stats["attack_animation_key"], stats["attack_frames"])
        
        # Asegurarse de que haya al menos un frame para cada animación
        if not self.animation_frames["idle"]:
            self.logger.log_error(f"No se encontraron frames para la animación Idle de {character_type}", "player")
            # Cargar un placeholder o salir
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(RED) # Placeholder rojo
        else:
            self.image = self.animation_frames["idle"][0] # Establecer el primer frame como imagen inicial

        self.logger.log_event(f"Personaje seleccionado: {character_type} con vidas={self.lives}, velocidad={self.speed}, shot_delay={self.shot_delay}", "player")

    def set_attack_type(self, attack_type):
        if attack_type in ATTACK_TYPES:
            self.attack_type = attack_type
            self.logger.log_event(f"Tipo de ataque cambiado a: {attack_type}", "player")
        else:
            self.logger.log_error(f"Tipo de ataque desconocido: {attack_type}", "player")

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.facing_left = True # Mover a la izquierda, mirar a la izquierda
            moving = True
        if keys[pygame.K_d]:
            self.x += self.speed
            self.facing_left = False # Mover a la derecha, mirar a la derecha
            moving = True
        # Limitar el movimiento a la pantalla
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.collision_box.topleft = (self.x, self.y)

        # Actualizar animación
        if moving:
            self.current_animation = "run"
        else:
            self.current_animation = "idle"

        current_time = time.time()
        if current_time - self.last_frame_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.current_animation])
            self.image = self.animation_frames[self.current_animation][self.current_frame]
            self.last_frame_update = current_time

        # Update power-up timers
        if self.is_fast_shooting and time.time() - self.fast_shot_timer > self.fast_shot_duration:
            self.is_fast_shooting = False
            self.shot_delay = self.original_shot_delay # Reset to normal
            self.logger.log_event("Power-up de disparo rápido terminado.", "player")

        if self.has_shield and time.time() - self.shield_timer > self.shield_duration:
            self.has_shield = False
            self.logger.log_event("Power-up de escudo terminado.", "player")

    def shoot(self, target_x, target_y):
        current_time = time.time()
        if current_time - self.last_shot_time > self.shot_delay:
            attack_props = ATTACK_TYPES[self.attack_type]
            projectile_size = attack_props["projectile_size"]
            projectile_speed = self.projectile_speed 
            projectile_image_path = attack_props["image"]
            projectile_piercing = attack_props["piercing"]
            projectile_damage = attack_props["damage"]

            # Cambiar a animación de disparo
            self.current_animation = "shoot"
            self.current_frame = 0 # Reiniciar animación de disparo

            projectile = Projectile(self.x + self.size // 2, self.y, target_x, target_y, 
                                    size=projectile_size, speed=projectile_speed, 
                                    image_path=projectile_image_path, piercing=projectile_piercing, 
                                    damage=projectile_damage, logger=self.logger)
            self.projectiles.append(projectile)

            self.logger.log_debug(f"Jugador disparó proyectil hacia x={target_x}, y={target_y} con ataque {self.attack_type}", "player")
            if self.sound_manager:
                self.sound_manager.play_sound("shoot")
            self.last_shot_time = current_time
            return [projectile]
        return []

    def draw(self, screen):
        # Dibujar el sprite actual del jugador
        scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        # Voltear la imagen si el jugador está mirando a la izquierda
        if self.facing_left:
            scaled_image = pygame.transform.flip(scaled_image, True, False)
        screen.blit(scaled_image, (self.x, self.y))
        print(f"[DEBUG] Dibujando jugador en ({self.x},{self.y})")

        if self.has_shield:
            pygame.draw.circle(screen, BLUE, (int(self.x + self.size / 2), int(self.y + self.size / 2)), self.size, 3) # Dibujar escudo
        for projectile in self.projectiles:
            projectile.draw(screen)

    def lose_life(self, amount=1):
        """Reduce las vidas del jugador o elimina corazones azules si hay escudo."""
        if self.has_shield and self.shield_lives > 0:
            self.shield_lives -= 1
            if self.shield_lives == 0:
                self.has_shield = False
            self.logger.log_event("Escudo absorbió el daño. Corazón azul eliminado.", "player")
            return
        if self.lives > 0:
            self.lives -= amount
            self.logger.log_event(f"Jugador pierde vida. Vidas restantes: {self.lives}", "player")

    def take_damage(self, amount=1):
        """Aplica daño al jugador, gestionando escudo y vidas."""
        self.logger.log_event(f"Jugador recibe daño: {amount}", "player")
        self.lose_life(amount)

    def activate_powerup(self, powerup_type):
        if powerup_type == "health":
            if self.lives < 3:
                self.lives += 1
                self.logger.log_event("Power-up de salud recogido! Vida añadida.", "player")
        elif powerup_type == "fast_shot":
            self.is_fast_shooting = True
            self.fast_shot_timer = time.time()
            self.shot_delay = 0.1 # Faster shooting
            self.logger.log_event("Power-up de disparo rápido activado!", "player")
        elif powerup_type == "shield":
            self.has_shield = True
            if not hasattr(self, 'shield_lives'):
                self.shield_lives = 0
            self.shield_lives += 1
            self.shield_timer = time.time()
            self.logger.log_event("Power-up de escudo activado! Corazón azul añadido.", "player")

    def get_upgrade_level(self, upgrade_key):
        """Devuelve el nivel actual de una mejora específica."""
        if hasattr(self, "upgrades") and upgrade_key in self.upgrades:
            return self.upgrades[upgrade_key].get("level", 0)
        return 0

    def draw_lives(self, screen):
        # Dibujar corazones rojos para las vidas
        heart_x_offset = 10
        for i in range(self.lives):
            heart_image = pygame.image.load("assets/ui/Hearts_Red_1.png")
            screen.blit(heart_image, (heart_x_offset, 10))
            heart_x_offset += heart_image.get_width() + 5

        # Dibujar corazones azules para el escudo
        for i in range(self.shield_lives):
            shield_image = pygame.image.load("assets/ui/Hearts_Blue_1.png")
            screen.blit(shield_image, (heart_x_offset, 10))
            heart_x_offset += shield_image.get_width() + 5
