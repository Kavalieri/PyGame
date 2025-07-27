from entities.enemy import Enemy
from constants import *

class BasicEnemy(Enemy):
    def __init__(self, x, y, logger=None):
        super().__init__(x, y, size=ENEMY_SIZE, speed=ENEMY_SPEED, image_path="assets/images/objects/Skeleton.png", health=1, logger=logger)

class FastEnemy(Enemy):
    def __init__(self, x, y, logger=None):
        super().__init__(x, y, size=ENEMY_SIZE - 10, speed=ENEMY_SPEED * 1.5, image_path="assets/images/objects/Skeleton.png", health=1, logger=logger)

class ToughEnemy(Enemy):
    def __init__(self, x, y, logger=None):
        super().__init__(x, y, size=ENEMY_SIZE + 10, speed=ENEMY_SPEED * 0.7, image_path="assets/images/objects/Skeleton.png", health=3, logger=logger)