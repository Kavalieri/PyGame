import random
import time
from src.entities.enemies import BasicEnemy, FastEnemy, ToughEnemy
from src.core.constants import *

class EnemyGenerator:
    def __init__(self, logger):
        self.logger = logger
        self.start_time = time.time()
        self.base_enemy_count = 4
        self.last_spawn_time = time.time()
        self.spawn_interval = 2  # Generar enemigos cada 2 segundos

    def generate_enemies(self, score):
        """Genera enemigos basados en la puntuación y el tiempo transcurrido."""
        new_enemies = []
        elapsed_time = time.time() - self.start_time
        time_based_extra = (elapsed_time // 60) * 2  # Añadir 2 enemigos extra cada minuto
        score_based_multiplier = 2 ** (score // 5)  # Duplicar cada 5 puntos
        max_enemies_to_spawn = self.base_enemy_count * score_based_multiplier + time_based_extra

        self.logger.log_debug(f"Generando enemigos: score={score}, max_enemies_to_spawn={max_enemies_to_spawn}")

        # Generar enemigos periódicamente
        if time.time() - self.last_spawn_time >= self.spawn_interval:
            enemy_type = random.choice([BasicEnemy, FastEnemy, ToughEnemy])
            enemy = enemy_type(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), 0, logger=self.logger)
            new_enemies.append(enemy)
            self.logger.log_debug(f"Enemigo generado en posición x={enemy.x}, y={enemy.y}")
            self.last_spawn_time = time.time()

        return new_enemies
