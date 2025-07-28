# PyGame - Juego de Disparos 2D

![Pygame Logo](https://raw.githubusercontent.com/pygame/pygame/main/docs/reST/pygame_logo.rst)

Este es un emocionante juego 2D de disparos desarrollado con Pygame. Sumérgete en un bucle de juego progresivo donde tu objetivo principal es destruir hordas de enemigos que descienden desde la parte superior de la pantalla, mientras mejoras tus habilidades y equipamiento.

## 🎮 Características Destacadas

### **Sistema de Juego Completo**
*   **Bucle de juego robusto**: Desde selección de personaje hasta fin de partida sin interrupciones
*   **Sistema de pausa dinámico**: Pulsa `P` o `ESC` en cualquier momento para pausar el juego
*   **Pantalla de fin de juego**: Muestra puntuación final y opciones de continuar

### **Sistema de Vida y Escudo**
*   **Corazones del jugador**: 3 corazones rojos que se vacían de derecha a izquierda
*   **Corazones azules de escudo**: Se añaden a la derecha y desaparecen completamente al recibir daño
*   **Barras de vida de enemigos**: Escalado porcentual con assets Health_03 según rareza

### **Enemigos y Combate**
*   **Enemigos variados**: Zombies masculinos y femeninos con diferentes patrones de movimiento
*   **Sistema de rarezas**: Normal, Raro, Élite y Legendario con estadísticas mejoradas
*   **Barras de vida visuales**: Roja (normal), Naranja (raro), Azul (élite/legendario)

### **Sistema de Mejoras Integrado**
*   **Menú de mejoras**: Aparece al finalizar cada nivel con puntos disponibles y gastados
*   **Mejoras progresivas**: Velocidad, vidas, cadencia de disparo, velocidad de proyectiles
*   **Ataques especiales**: Disparo de ráfaga y disparo penetrante
*   **Sistema de reset**: Permite reiniciar mejoras y recuperar puntos gastados

### **Personajes y Progresión**
*   **Selección de personajes**: Kava (guerrero), Sara (sacerdote), Guiral (mago)
*   **Estadísticas únicas**: Cada personaje tiene velocidad, vidas y cadencia de disparo diferentes
*   **Animaciones completas**: Idle, run, walk, attack para cada personaje

### **Sistema de Guardado**
*   **Guardado y carga**: 3 slots de guardado con estado completo del juego
*   **Persistencia de datos**: Puntuación, nivel, mejoras y estado del jugador

## 🌐 Idioma

El idioma principal del código, los comentarios y toda la comunicación del proyecto es el **español**.

## 🛠️ Dependencias

Para instalar todas las dependencias necesarias y poder ejecutar el juego, utiliza el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🚀 Cómo Ejecutar el Juego

El punto de entrada de la aplicación es `main.py`. Para iniciar tu aventura, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python src/main.py
```

## 🎯 Controles del Juego

*   **Movimiento**: `A` (izquierda) y `D` (derecha)
*   **Disparo**: Clic izquierdo del ratón
*   **Pausa**: `P` o `ESC`
*   **Navegación de menús**: Flechas direccionales + `Enter` o clic del ratón

## 🏗️ Arquitectura del Proyecto

```
src/
├── main.py                 # Punto de entrada principal
├── game_loop.py           # Bucle principal del juego
├── constants.py           # Constantes y configuraciones
├── entities/              # Entidades del juego
│   ├── player.py         # Jugador y lógica de personajes
│   ├── enemy.py          # Enemigos y barras de vida
│   ├── projectile.py     # Proyectiles del jugador y enemigos
│   └── powerups.py       # Power-ups y efectos
├── managers/              # Gestores del sistema
│   ├── enemy_generator.py # Generación de enemigos
│   ├── sound_manager.py   # Gestión de audio
│   ├── save_manager.py    # Sistema de guardado
│   └── logger.py         # Sistema de logging
├── ui/                    # Interfaz de usuario
│   ├── hud.py            # HUD y corazones
│   └── menus/            # Menús del juego
│       ├── base_menu.py  # Menú base reutilizable
│       ├── menu.py       # Menú principal
│       ├── upgrade_menu.py # Menú de mejoras
│       └── character_selection_menu.py # Selección de personaje
└── utils/                 # Utilidades
    └── image_loader.py   # Cargador de imágenes y animaciones
```

## 🤝 Contribución y Colaboración

¡Nos encantaría contar con tu ayuda para mejorar este proyecto! Para mantener la consistencia y la calidad del código, y para entender cómo puedes contribuir, por favor, consulta nuestra guía detallada de colaboración:

➡️ [Guía de Colaboración](docs/COLABORACION.md)

## 📝 Notas de Desarrollo

* **Versión**: Proyecto base funcional
* **Estado**: Jugable completo con todas las funcionalidades básicas
* **Próximas mejoras**: Refinamiento visual, balance de juego y nuevas características

---