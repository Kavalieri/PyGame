import pygame
import os

def darken_image(image_path, output_path, darken_factor=0.6):
    pygame.init()
    # Inicializar una superficie de pantalla mínima para permitir la carga de imágenes
    screen = pygame.display.set_mode((1, 1), pygame.HIDDEN)

    try:
        original_image = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {e}")
        pygame.quit()
        return

    darkened_image = original_image.copy()
    darkened_image.fill((0, 0, 0, int(255 * darken_factor)), special_flags=pygame.BLEND_RGBA_MULT)

    pygame.image.save(darkened_image, output_path)
    print(f"Image darkened and saved to: {output_path}")

    pygame.quit()

if __name__ == "__main__":
    base_path = "c:/Users/Kava/Documents/GitHub/PyGame/"
    input_path = os.path.join(base_path, "assets/images/fondos/game_background_1.png")
    output_path = os.path.join(base_path, "assets/images/fondos/game_background_1_dark.png")
    darken_image(input_path, output_path, darken_factor=0.6) # Ajusta darken_factor segn sea necesario