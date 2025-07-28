# PyGame Shooter

**Autor:** Kava
**Fecha:** 2024-12-19

## Descripción
Juego 2D de disparos desarrollado con pygame-ce. El objetivo es destruir enemigos que caen desde la parte superior de la pantalla, con sistema de upgrades, menús avanzados y logging profesional.

## Características principales
- Bucle de juego optimizado y modular
- Menús avanzados con pygame-menu
- HUD y renderizado de texto con ptext
- Físicas y animaciones optimizadas
- Sistema de logging avanzado por componente
- Guardado/carga de partidas con múltiples slots
- Gestión de assets y sonidos profesional

## Instalación
1. Clona el repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el juego:
   ```bash
   python src/main.py
   ```

## Estructura del proyecto
- `src/` - Código fuente principal
- `assets/` - Assets en uso (imágenes, sonidos, fuentes)
- `logs/` - Archivos de log generados automáticamente
- `tools/` - Herramientas y scripts auxiliares
- `docs/` - Documentación y colaboración

## Changelog
### 2024-12-19 (v2.0)
- Migración completa a sistema de logging avanzado (Python logging)
- Refactorización modular de todos los componentes
- Menús avanzados y HUD profesional
- Eliminación de código y logs obsoletos
- Documentación y cabeceras actualizadas (autor: Kava)

## Contribución
Las contribuciones son bienvenidas. Por favor, revisa `docs/COLABORACION.md` para las normas y recomendaciones de colaboración.

## Licencia
Este proyecto está bajo la licencia MIT.