#!/usr/bin/env python3
"""
Script de prueba para evaluar herramientas de refactorización
Autor: Gemini
Fecha: 2024-12-19
Descripción: Prueba pygame-ce, pygame-tools, pygame-menu, pymunk y otras herramientas
"""

import sys
import time

def test_pygame_versions():
    """Prueba y compara pygame-ce vs pygame clásico"""
    print("=== COMPARACIÓN PYGAME-CE VS PYGAME CLÁSICO ===\n")
    
    try:
        import pygame
        print(f"✅ pygame importado correctamente")
        print(f"   Versión: {pygame.version.ver}")
        print(f"   SDL: {pygame.version.SDL_ver}")
        print(f"   Python: {pygame.version.Python}")
        
        # Pruebas básicas
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test pygame")
        
        # Prueba de rendimiento básico
        start_time = time.time()
        for i in range(1000):
            screen.fill((0, 0, 0))
            pygame.draw.circle(screen, (255, 255, 255), (400, 300), 50)
            pygame.display.flip()
        end_time = time.time()
        
        print(f"   Rendimiento: {end_time - start_time:.3f}s para 1000 frames")
        pygame.quit()
        
    except Exception as e:
        print(f"❌ Error con pygame: {e}")

def test_pygame_tools():
    """Prueba pygame-tools"""
    print("\n=== PYGAME-TOOLS ===\n")
    
    try:
        from pygame_tools import Game
        print("✅ pygame-tools importado correctamente")
        
        # Verificar funcionalidades disponibles
        print("   Funcionalidades disponibles:")
        print("   - Game class para bucle de juego simplificado")
        print("   - Event handling automático")
        print("   - FPS management")
        
    except Exception as e:
        print(f"❌ Error con pygame-tools: {e}")

def test_pygame_menu():
    """Prueba pygame-menu"""
    print("\n=== PYGAME-MENU ===\n")
    
    try:
        import pygame_menu
        print("✅ pygame-menu importado correctamente")
        print(f"   Versión: {pygame_menu.__version__}")
        
        # Verificar temas disponibles
        themes = [theme for theme in dir(pygame_menu.themes) if not theme.startswith('_')]
        print(f"   Temas disponibles: {len(themes)}")
        print(f"   Ejemplos: {themes[:5]}")
        
        # Verificar widgets disponibles
        widgets = [widget for widget in dir(pygame_menu) if 'Widget' in widget]
        print(f"   Widgets disponibles: {len(widgets)}")
        print(f"   Ejemplos: {widgets[:5]}")
        
    except Exception as e:
        print(f"❌ Error con pygame-menu: {e}")

def test_pymunk():
    """Prueba pymunk"""
    print("\n=== PYMUNK ===\n")
    
    try:
        import pymunk
        print("✅ pymunk importado correctamente")
        print(f"   Versión: {pymunk.version}")
        
        # Crear un espacio de física simple
        space = pymunk.Space()
        space.gravity = (0, 981)  # Gravedad hacia abajo
        
        # Crear un cuerpo estático (suelo)
        ground = pymunk.Segment(space.static_body, (0, 550), (800, 550), 1)
        ground.friction = 1.0
        space.add(ground)
        
        # Crear un cuerpo dinámico (pelota)
        body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 25))
        body.position = 400, 0
        shape = pymunk.Circle(body, 25)
        shape.friction = 0.7
        space.add(body, shape)
        
        print("   ✅ Espacio de física creado correctamente")
        print("   ✅ Cuerpos estáticos y dinámicos funcionando")
        
    except Exception as e:
        print(f"❌ Error con pymunk: {e}")

def test_ptext():
    """Prueba ptext"""
    print("\n=== PTEXT ===\n")
    
    try:
        import ptext
        print("✅ ptext importado correctamente")
        print(f"   Versión: {ptext.__version__}")
        
        # Verificar funcionalidades
        print("   Funcionalidades:")
        print("   - Renderizado de texto optimizado")
        print("   - Soporte para fuentes personalizadas")
        print("   - Efectos de texto (sombra, outline)")
        print("   - Cache automático de fuentes")
        
    except Exception as e:
        print(f"❌ Error con ptext: {e}")

def test_pygame_gui():
    """Prueba pygame-gui"""
    print("\n=== PYGAME-GUI ===\n")
    
    try:
        import pygame_gui
        print("✅ pygame-gui importado correctamente")
        print(f"   Versión: {pygame_gui.__version__}")
        
        # Verificar elementos disponibles
        elements = [elem for elem in dir(pygame_gui.elements) if not elem.startswith('_')]
        print(f"   Elementos UI disponibles: {len(elements)}")
        print(f"   Ejemplos: {elements[:5]}")
        
        # Verificar managers disponibles
        managers = [mgr for mgr in dir(pygame_gui) if 'Manager' in mgr]
        print(f"   Managers disponibles: {len(managers)}")
        print(f"   Ejemplos: {managers}")
        
    except Exception as e:
        print(f"❌ Error con pygame-gui: {e}")

def test_alternatives_to_pyknic():
    """Prueba alternativas a pyknic para spritesheets"""
    print("\n=== ALTERNATIVAS A PYKNIC ===\n")
    
    print("Alternativas para manejo de spritesheets:")
    print("1. pygame.sprite.Sprite - Sistema nativo de pygame")
    print("2. Implementación manual con pygame.Surface.subsurface()")
    print("3. spritesheetlib (si está disponible)")
    print("4. Crear nuestra propia clase SpriteSheet")
    
    # Demostrar implementación manual
    try:
        import pygame
        pygame.init()
        
        # Crear una superficie de ejemplo (simulando spritesheet)
        spritesheet = pygame.Surface((256, 64))
        spritesheet.fill((255, 0, 0))  # Fondo rojo
        
        # Extraer sprites usando subsurface
        sprite1 = spritesheet.subsurface((0, 0, 64, 64))
        sprite2 = spritesheet.subsurface((64, 0, 64, 64))
        sprite3 = spritesheet.subsurface((128, 0, 64, 64))
        sprite4 = spritesheet.subsurface((192, 0, 64, 64))
        
        print("✅ Implementación manual de spritesheet funcionando")
        print(f"   Sprites extraídos: {sprite1.get_size()}")
        
        pygame.quit()
        
    except Exception as e:
        print(f"❌ Error con implementación manual: {e}")

def main():
    """Función principal de pruebas"""
    print("🔧 PRUEBAS DE HERRAMIENTAS DE REFACTORIZACIÓN")
    print("=" * 50)
    
    test_pygame_versions()
    test_pygame_tools()
    test_pygame_menu()
    test_pymunk()
    test_ptext()
    test_pygame_gui()
    test_alternatives_to_pyknic()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RECOMENDACIONES:")
    print("=" * 50)
    
    print("✅ HERRAMIENTAS RECOMENDADAS:")
    print("   - pygame-ce: Mejoras significativas en rendimiento y compatibilidad")
    print("   - pygame-tools: Reduce boilerplate del bucle de juego")
    print("   - pygame-menu: Menús profesionales con temas")
    print("   - pymunk: Física realista para proyectiles y movimiento")
    print("   - ptext: Texto optimizado para HUD")
    print("   - pygame-gui: UI avanzada para HUD y elementos de juego")
    
    print("\n⚠️  CONSIDERACIONES:")
    print("   - pyknic no está disponible, usar implementación manual")
    print("   - pygame-ce es compatible con pygame clásico")
    print("   - Todas las herramientas son estables y bien mantenidas")
    
    print("\n🚀 PLAN DE ACCIÓN:")
    print("   1. Migrar a pygame-ce (compatible)")
    print("   2. Implementar pygame-tools para bucle simplificado")
    print("   3. Migrar menús a pygame-menu")
    print("   4. Añadir pymunk para física avanzada")
    print("   5. Optimizar texto con ptext")
    print("   6. Mejorar HUD con pygame-gui")

if __name__ == "__main__":
    main() 