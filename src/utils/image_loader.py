import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_image(path, alpha=True):
    full_path = resource_path(path)
    try:
        image = pygame.image.load(full_path)
        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image
    except pygame.error as message:
        print(f"No se pudo cargar la imagen: {full_path}")
        raise SystemExit(message)

def load_animation_frames(base_folder, animation_name, num_frames, alpha=True):
    frames = []
    for i in range(1, num_frames + 1):
        # Intentar cargar desde un subdirectorio (ej. assets/images/characters/guerrero/idle/Idle (1).png)
        animation_folder_path = os.path.join(base_folder, animation_name.lower())
        frame_path_in_subfolder = os.path.join(animation_folder_path, f"{animation_name} ({i}).png")
        
        # Intentar cargar directamente desde la carpeta base (ej. assets/images/characters/adventureguirl/Idle (1).png)
        frame_path_in_base_folder = os.path.join(base_folder, f"{animation_name} ({i}).png")

        try:
            if os.path.exists(resource_path(frame_path_in_subfolder)):
                frames.append(load_image(frame_path_in_subfolder, alpha))
            elif os.path.exists(resource_path(frame_path_in_base_folder)):
                frames.append(load_image(frame_path_in_base_folder, alpha))
            else:
                print(f"Advertencia: No se encontró el frame {i} para la animación {animation_name} en {base_folder}. Intentando {frame_path_in_subfolder} y {frame_path_in_base_folder}")
                continue
        except SystemExit:
            # load_image ya imprime un error, así que solo continuamos
            continue
    return frames
