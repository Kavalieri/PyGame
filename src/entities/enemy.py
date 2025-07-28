import pygame
import random
import time
from constants import *
from entities.projectile import Projectile
from utils.image_loader import load_image, load_animation_frames

class Enemy:
    def __init__(self, x, y, enemy_type, rarity="NORMAL", logger=None):
        self.x = x
        self.y = y
        self.logger = logger
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

        if self.logger:
            self.logger.log_debug(f"Enemigo {enemy_type} ({rarity}) creado en posición x={self.x}, y={self.y}, tamaño={self.size}, velocidad={self.speed}, salud={self.health}, can_shoot={self.can_shoot}")
            self.logger.log_debug(f"Health frame image: {self.health_frame_image}, Health bar image: {self.health_bar_image}")

    def move(self):
        self.y += self.speed

        if self.movement_pattern == "zigzag":
            # Mover horizontalmente en zigzag
            self.x += self.zigzag_direction * self.speed * self.zigzag_speed_multiplier
            # Cambiar dirección si alcanza los límites
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
                self.zigzag_direction *= -1

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

        # Dibujar barra de vida
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        # Dibujar el marco de la barra de vida
        frame_width = self.health_frame_image.get_width()
        frame_height = self.health_frame_image.get_height()
        frame_x = self.x
        frame_y = self.y - frame_height - 5
        screen.blit(self.health_frame_image, (frame_x, frame_y))

        # Dibujar la barra de vida con tamaño fijo del marco, solo recortando porcentualmente
        bar_width = self.health_bar_image.get_width()
        bar_height = self.health_bar_image.get_height()
        health_ratio = max(0, self.health / self.base_health)
        bar_draw_width = int(bar_width * health_ratio)
        
        # La barra siempre se dibuja en la posición del marco, solo se recorta el ancho
        if bar_draw_width > 0 and bar_draw_width <= bar_width:
            bar_image = self.health_bar_image.subsurface((0, 0, bar_draw_width, bar_height))
            # Centrar la barra dentro del marco
            bar_x = frame_x + (frame_width - bar_width) // 2
            bar_y = frame_y + (frame_height - bar_height) // 2
            screen.blit(bar_image, (bar_x, bar_y))

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def take_damage(self, damage):
        self.health -= damage
        if self.logger:
            self.logger.log_debug(f"Enemigo en x={self.x}, y={self.y} recibió {damage} de daño. Salud restante: {self.health}")

        # Mostrar daño recibido
        font = pygame.font.Font(None, 24)
        damage_text = font.render(f"-{damage}", True, (255, 0, 0))
        screen = pygame.display.get_surface()
        screen.blit(damage_text, (self.x + self.size // 2, self.y - 20))

        return self.health <= 0

    def on_defeat(self):
        # Mostrar puntos sumados
        font = pygame.font.Font(None, 24)
        points_text = font.render(f"+{self.score_value}", True, (0, 255, 0))
        screen = pygame.display.get_surface()
        screen.blit(points_text, (self.x + self.size // 2, self.y - 20))