#!/usr/bin/env python3
"""
Generador de enemigos para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Lógica de generación dinámica de enemigos según el progreso y puntuación del jugador.
"""
import random
import time
from entities.enemy import Enemy # Importar la clase Enemy genérica
from constants import *
from utils.advanced_logger import get_logger

class EnemyGenerator:
    def __init__(self, logger=None):
        self.logger = logger or get_logger("PyGame")
        self.start_time = time.time()
        self.base_enemy_count = 4
        self.last_spawn_time = time.time()
        self.spawn_interval = 2  # Generar enemigos cada 2 segundos
        self.logger.log_event("EnemyGenerator inicializado", "enemy_gen")

    def generate_enemies(self, score):
        """Genera enemigos basados en la puntuación y el tiempo transcurrido."""
        new_enemies = []
        elapsed_time = time.time() - self.start_time
        time_based_extra = (elapsed_time // 60) * 2  # Añadir 2 enemigos extra cada minuto
        score_based_multiplier = 2 ** (score // 5)  # Duplicar cada 5 puntos
        max_enemies_to_spawn = self.base_enemy_count * score_based_multiplier + time_based_extra

        self.logger.log_debug(f"Generando enemigos: score={score}, max_enemies_to_spawn={max_enemies_to_spawn}", "enemy_gen")

        # Generar enemigos periódicamente
        if time.time() - self.last_spawn_time >= self.spawn_interval:
            # Seleccionar tipo de enemigo aleatoriamente
            enemy_type_name = random.choice(["ZOMBIE_MALE", "ZOMBIE_GIRL"])
            
            # Seleccionar rareza del enemigo
            rarity_choices = [rarity for rarity, prob in RARITY_PROBABILITIES.items() for _ in range(int(prob * 100))]
            enemy_rarity = random.choice(rarity_choices)

            enemy = Enemy(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), 0, enemy_type=enemy_type_name, rarity=enemy_rarity, logger=self.logger)
            new_enemies.append(enemy)
            self.logger.log_debug(f"Enemigo generado: Tipo={enemy_type_name}, Rareza={enemy_rarity}, Posición=({enemy.x}, {enemy.y})", "enemy_gen")
            self.last_spawn_time = time.time()

        return new_enemies
