import shutil
import os

copy_tasks = [
    {"source": "full_assets/images/Simple Game UI Pack #1 - Rebuild", "destination": "assets/images/ui/Simple Game UI Pack #1 - Rebuild"},
    {"source": "full_assets/images/SimpleUI", "destination": "assets/images/ui/SimpleUI"},
    {"source": "full_assets/images/UI Kit 1", "destination": "assets/images/ui/UI Kit 1"}
]

for task in copy_tasks:
    source_dir = task["source"]
    dest_dir = task["destination"]

    # Asegurarse de que el directorio de destino exista
    os.makedirs(dest_dir, exist_ok=True)

    try:
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        print(f"Copiado exitosamente: {source_dir} a {dest_dir}")
    except Exception as e:
        print(f"Error al copiar {source_dir} a {dest_dir}: {e}")