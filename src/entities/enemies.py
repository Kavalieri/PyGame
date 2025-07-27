from src.entities.enemy import Enemy
from src.core.constants import *

class BasicEnemy(Enemy):
    def __init__(self, x, y, logger=None):
        super().__init__(x, y, size=ENEMY_SIZE, speed=ENEMY_SPEED, color=RED, health=1, logger=logger)

class FastEnemy(Enemy):
    def __init__(self, x, y, logger=None):
        super().__init__(x, y, size=ENEMY_SIZE - 10, speed=ENEMY_SPEED * 1.5, color=BLUE, health=1, logger=logger)

class ToughEnemy(Enemy):
    def __init__(self, x, y, logger=None):
        super().__init__(x, y, size=ENEMY_SIZE + 10, speed=ENEMY_SPEED * 0.7, color=GREEN, health=3, logger=logger)
