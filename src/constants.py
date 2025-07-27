# Constantes del juego

# Pantalla
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Jugador
PLAYER_SIZE = 128 # Aumentado para que se vea más grande
PLAYER_SPEED = 5
PLAYER_LIVES = 3

# Proyectiles
PROJECTILE_SIZE = 32 # Ajustado para los sprites
PROJECTILE_SPEED = 10

# Enemigos
ENEMY_SIZE = 96 # Ajustado para los sprites
ENEMY_SPEED = 2
ENEMY_HEALTH = 1

# Power-ups
POWERUP_SIZE = 30
POWERUP_SPEED = 3
FAST_SHOT_DURATION = 5 # segundos
SHIELD_DURATION = 10 # segundos

# Niveles (ejemplo)
LEVELS = {
    1: {"duration": 30, "enemy_spawn_rate": 100}, # Cada 100 frames
    2: {"duration": 45, "enemy_spawn_rate": 80},
    3: {"duration": 60, "enemy_spawn_rate": 60},
}

# Estadísticas de personajes
CHARACTER_STATS = {
    "Kava": {
        "name": "Kava el Guerrero",
        "description": "Un guerrero fuerte y resistente, ideal para el combate cuerpo a cuerpo.",
        "speed": 5,
        "lives": 4,
        "shot_delay": 0.6,
        "image_folder": "assets/images/characters/guerrero",
        "idle_frames": 10, 
        "run_frames": 8, 
        "walk_frames": 8, # Añadido walk_frames para Kava
        "attack_frames": 10,
        "attack_animation_key": "Attack" # Usar la animación 'Attack' para Kava
    },
    "Sara": {
        "name": "Sara la Sacerdote",
        "description": "Una sacerdotisa ágil con disparos rápidos y habilidades de apoyo.",
        "speed": 7,
        "lives": 2,
        "shot_delay": 0.3,
        "image_folder": "assets/images/characters/adventureguirl",
        "idle_frames": 10, 
        "run_frames": 8, 
        "attack_frames": 7,
        "attack_animation_key": "Shoot" # Usar la animación 'Shoot' para Sara
    },
    "Guiral": {
        "name": "Guiral el Mago",
        "description": "Un mago poderoso con ataques de área y gran daño.",
        "speed": 4,
        "lives": 3,
        "shot_delay": 0.7,
        "image_folder": "assets/images/characters/robot",
        "idle_frames": 10, 
        "run_frames": 8, 
        "attack_frames": 4, # Corregido a 4 frames para Shoot
        "attack_animation_key": "Shoot" # Usar la animación 'Shoot' para Guiral
    }
}

# Tipos de ataque
ATTACK_TYPES = {
    "normal": {
        "projectile_size": 32,
        "projectile_speed": 10,
        "image": "assets/images/objects/proyectiles/aranazo.png", # Usar sprite
        "piercing": False,
        "damage": 1
    },
    "spread_shot": {
        "projectile_size": 32,
        "projectile_speed": 8,
        "image": "assets/images/objects/proyectiles/aranazo2.png", # Usar sprite
        "piercing": False,
        "damage": 1,
        "num_projectiles": 3,
        "angle_spread": 0.3 # radians
    },
    "piercing_shot": {
        "projectile_size": 32,
        "projectile_speed": 12,
        "image": "assets/images/objects/proyectiles/aranazo.png", # Usar sprite
        "piercing": True,
        "damage": 2
    }
}

# Mejoras
UPGRADES = {
    "player_speed": {
        "name": "Velocidad del Jugador",
        "description": "Aumenta la velocidad de movimiento del jugador.",
        "cost": 50,
        "effect": {"speed": 1}
    },
    "player_lives": {
        "name": "Vida Extra",
        "description": "Otorga una vida adicional al jugador.",
        "cost": 100,
        "effect": {"lives": 1}
    },
    "shot_delay_reduction": {
        "name": "Cadencia de Disparo",
        "description": "Reduce el tiempo entre disparos.",
        "cost": 75,
        "effect": {"shot_delay": -0.05}
    },
    "projectile_speed_increase": {
        "name": "Velocidad de Proyectil",
        "description": "Aumenta la velocidad de los proyectiles.",
        "cost": 60,
        "effect": {"projectile_speed": 1}
    },
    "attack_spread_shot": {
        "name": "Disparo de Ráfaga",
        "description": "Desbloquea el disparo de ráfaga.",
        "cost": 150,
        "effect": {"attack_type": "spread_shot"}
    },
    "attack_piercing_shot": {
        "name": "Disparo Penetrante",
        "description": "Desbloquea el disparo penetrante.",
        "cost": 200,
        "effect": {"attack_type": "piercing_shot"}
    }
}

# Fondos
BACKGROUND_IMAGES = [
    "assets/images/fondos/game_background_1_dark.png"
]

# Enemigos
ENEMY_TYPES = {
    "Basic": {
        "image_folder": "assets/images/characters/robot",
        "idle_frames": 10, # Asumiendo 10 frames para Idle
        "run_frames": 8, # Corregido a 8 frames para Run
        "attack_frames": 4, # Corregido a 4 frames para Attack (Shoot)
        "attack_animation_key": "Shoot", # Añadido para Basic
        "health": 1,
        "speed": 2,
        "size": ENEMY_SIZE,
        "color_palette": "normal" # Para futuras variaciones de color
    },
    "Tough": {
        "image_folder": "assets/images/characters/zombieguirl",
        "idle_frames": 15, 
        "run_frames": 10, 
        "attack_frames": 8, 
        "run_animation_key": "Walk", # Añadido para zombieguirl
        "attack_animation_key": "Attack", # Añadido para zombieguirl
        "health": 3,
        "speed": 1.5,
        "size": ENEMY_SIZE + 32,
        "color_palette": "greenish" # Para futuras variaciones de color
    },
    "Fast": {
        "image_folder": "assets/images/characters/robot",
        "idle_frames": 10, 
        "run_frames": 8, # Corregido a 8 frames para Run
        "attack_frames": 4, # Corregido a 4 frames para Attack (Shoot)
        "attack_animation_key": "Shoot", # Añadido para Fast
        "health": 1,
        "speed": 3.5,
        "size": ENEMY_SIZE - 16,
        "color_palette": "reddish" # Para futuras variaciones de color
    }
}
