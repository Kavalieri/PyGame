#!/usr/bin/env python3
"""
Script de prueba para verificar la refactorización
Autor: Gemini
Fecha: 2024-12-19
Descripción: Prueba todas las nuevas herramientas implementadas en la refactorización
"""

import sys
import os
import pygame
import time

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.sprite_sheet import SpriteSheet, AnimationManager
from utils.text_renderer import TextRenderer
from ui.menu_system import MenuSystem
from managers.logger import Logger


def test_pygame_ce():
    """Prueba que pygame-ce funciona correctamente."""
    print("=== PRUEBA PYGAME-CE ===")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test PyGame-CE")
        
        # Verificar versión
        print(f"✅ PyGame versión: {pygame.version.ver}")
        
        # Prueba básica de renderizado
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 50)
        pygame.display.flip()
        
        # Esperar un momento
        time.sleep(1)
        
        pygame.quit()
        print("✅ PyGame-CE funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con PyGame-CE: {e}")
        return False


def test_sprite_sheet():
    """Prueba la clase SpriteSheet."""
    print("\n=== PRUEBA SPRITESHEET ===")
    
    try:
        pygame.init()
        pygame.display.set_mode((800, 600))  # Inicializar display para convert_alpha
        
        logger = Logger()
        
        # Crear una superficie de prueba (simulando spritesheet)
        test_sheet = pygame.Surface((256, 64))
        test_sheet.fill((255, 0, 0))  # Fondo rojo
        
        # Guardar temporalmente para probar
        pygame.image.save(test_sheet, "temp_test_sheet.png")
        
        # Probar SpriteSheet
        spritesheet = SpriteSheet("temp_test_sheet.png", logger)
        
        # Probar extracción de sprites
        sprite1 = spritesheet.get_sprite(0, 0, 64, 64)
        sprite2 = spritesheet.get_sprite(64, 0, 64, 64)
        
        print(f"✅ SpriteSheet creado - Tamaño: {spritesheet.get_sheet_size()}")
        print(f"✅ Sprites extraídos: {sprite1.get_size()}, {sprite2.get_size()}")
        
        # Probar animación
        animation = spritesheet.get_animation(0, 0, 64, 64, 4)
        print(f"✅ Animación creada: {len(animation)} frames")
        
        # Limpiar archivo temporal
        os.remove("temp_test_sheet.png")
        pygame.quit()
        
        print("✅ SpriteSheet funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con SpriteSheet: {e}")
        return False


def test_animation_manager():
    """Prueba el AnimationManager."""
    print("\n=== PRUEBA ANIMATION MANAGER ===")
    
    try:
        pygame.init()
        pygame.display.set_mode((800, 600))  # Inicializar display
        
        logger = Logger()
        anim_manager = AnimationManager(logger)
        
        # Crear superficie de prueba
        test_sheet = pygame.Surface((256, 64))
        test_sheet.fill((0, 255, 0))  # Fondo verde
        pygame.image.save(test_sheet, "temp_anim_sheet.png")
        
        # Cargar spritesheet
        success = anim_manager.load_spritesheet("test", "temp_anim_sheet.png")
        print(f"✅ Spritesheet cargado: {success}")
        
        # Crear animación
        success = anim_manager.create_animation("test_anim", "test", 0, 0, 64, 64, 4)
        print(f"✅ Animación creada: {success}")
        
        # Obtener animación
        animation = anim_manager.get_animation("test_anim")
        print(f"✅ Animación obtenida: {len(animation)} frames")
        
        # Limpiar
        anim_manager.clear_all()
        os.remove("temp_anim_sheet.png")
        pygame.quit()
        
        print("✅ AnimationManager funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con AnimationManager: {e}")
        return False


def test_text_renderer():
    """Prueba el TextRenderer con ptext."""
    print("\n=== PRUEBA TEXT RENDERER ===")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        logger = Logger()
        text_renderer = TextRenderer(logger)
        
        # Probar renderizado básico
        text_renderer.render_text("Test Text", (100, 100))
        print("✅ Texto básico renderizado")
        
        # Probar texto con sombra
        text_renderer.render_text("Shadow Text", (100, 150), shadow=True)
        print("✅ Texto con sombra renderizado")
        
        # Probar texto centrado
        text_renderer.render_centered_text("Centered Text", 200, screen_width=800)
        print("✅ Texto centrado renderizado")
        
        # Probar HUD específico
        text_renderer.render_score(1000, (100, 250))
        text_renderer.render_level(5, (100, 280))
        text_renderer.render_lives(3, (100, 310))
        print("✅ Textos de HUD renderizados")
        
        # Probar obtención de tamaño
        size = text_renderer.get_text_size("Test")
        print(f"✅ Tamaño de texto obtenido: {size}")
        
        pygame.quit()
        print("✅ TextRenderer funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con TextRenderer: {e}")
        return False


def test_menu_system():
    """Prueba el sistema de menús con pygame-menu."""
    print("\n=== PRUEBA MENU SYSTEM ===")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))  # Ventana más grande para los menús
        
        logger = Logger()
        menu_system = MenuSystem(screen, logger)
        
        # Probar creación de menús básicos (sin frames complejos)
        main_menu = menu_system.create_main_menu()
        print("✅ Menú principal creado")
        
        pause_menu = menu_system.create_pause_menu()
        print("✅ Menú de pausa creado")
        
        game_over_menu = menu_system.create_game_over_menu(1500)
        print("✅ Menú de fin de juego creado")
        
        options_menu = menu_system.create_options_menu()
        print("✅ Menú de opciones creado")
        
        # Probar callbacks
        def test_callback():
            print("✅ Callback ejecutado")
        
        menu_system.register_callback("test_action", test_callback)
        print("✅ Callback registrado")
        
        pygame.quit()
        print("✅ MenuSystem funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con MenuSystem: {e}")
        return False


def test_integration():
    """Prueba la integración de todas las herramientas."""
    print("\n=== PRUEBA DE INTEGRACIÓN ===")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))  # Ventana más grande
        
        logger = Logger()
        
        # Crear todas las herramientas
        text_renderer = TextRenderer(logger)
        menu_system = MenuSystem(screen, logger)
        anim_manager = AnimationManager(logger)
        
        # Crear spritesheet de prueba
        test_sheet = pygame.Surface((256, 64))
        test_sheet.fill((100, 100, 255))  # Fondo azul
        pygame.image.save(test_sheet, "temp_integration_sheet.png")
        
        # Cargar en AnimationManager
        anim_manager.load_spritesheet("integration", "temp_integration_sheet.png")
        anim_manager.create_animation("integration_anim", "integration", 0, 0, 64, 64, 4)
        
        # Renderizar texto
        text_renderer.render_title("Integración Exitosa", 50, 1280)
        text_renderer.render_subtitle("Todas las herramientas funcionan", 120, 1280)
        
        # Crear menú
        menu = menu_system.create_main_menu()
        
        # Mostrar información
        info_text = [
            f"TextRenderer: {len(text_renderer)} elementos en cache",
            f"AnimationManager: {len(anim_manager.spritesheets)} spritesheets",
            f"MenuSystem: {len(menu_system.callbacks)} callbacks registrados"
        ]
        
        for i, text in enumerate(info_text):
            text_renderer.render_hud_text(text, (50, 200 + i * 30))
        
        pygame.display.flip()
        time.sleep(3)  # Mostrar por 3 segundos
        
        # Limpiar
        anim_manager.clear_all()
        text_renderer.clear_cache()
        os.remove("temp_integration_sheet.png")
        pygame.quit()
        
        print("✅ Integración exitosa - Todas las herramientas funcionan juntas")
        return True
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return False


def main():
    """Función principal de pruebas."""
    print("🔧 PRUEBAS DE REFACTORIZACIÓN - FASE 1")
    print("=" * 50)
    
    tests = [
        ("PyGame-CE", test_pygame_ce),
        ("SpriteSheet", test_sprite_sheet),
        ("AnimationManager", test_animation_manager),
        ("TextRenderer", test_text_renderer),
        ("MenuSystem", test_menu_system),
        ("Integración", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS DE LAS PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResumen: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La refactorización está lista.")
        print("\n🚀 Próximos pasos:")
        print("1. Migrar el código existente a las nuevas herramientas")
        print("2. Implementar pymunk para física")
        print("3. Optimizar rendimiento general")
        print("4. Testing completo del juego")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar errores antes de continuar.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 