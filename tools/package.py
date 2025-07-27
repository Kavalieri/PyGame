import os
import sys
import subprocess
import shutil
import zipfile

def get_current_version():
    with open("VERSION.txt", "r") as f:
        return f.read().strip()

def update_version(version_type):
    current_version = get_current_version()
    major, minor, patch = map(int, current_version.split('.'))

    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        raise ValueError("Tipo de versión inválido. Use 'major', 'minor' o 'patch'.")

    new_version = f"{major}.{minor}.{patch}"
    with open("VERSION.txt", "w") as f:
        f.write(new_version)
    return new_version

def package_project(version):
    print(f"Empaquetando la versión {version}...")

    release_dir = os.path.join("releases", f"v{version}")
    os.makedirs(release_dir, exist_ok=True)

    # Limpiar directorios de compilación anteriores dentro del directorio de la versión
    build_dir = os.path.join(release_dir, "build")
    dist_dir = os.path.join(release_dir, "dist")

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    # Comando PyInstaller
    if sys.platform == "win32":
        data_sep = ";"
    else:
        data_sep = ":"

    # Obtener la ruta absoluta para assets
    assets_abs_path = os.path.abspath("assets")

    pyinstaller_command = [
        "pyinstaller",
        "src/main.py",
        "--noconsole",
        "--onefile",
        f"--add-data={assets_abs_path}{data_sep}assets", # Usar ruta absoluta para assets
        f"--paths=src",
        f"--name=PyGame_v{version}",
        f"--distpath={dist_dir}", # Ruta de salida para el ejecutable
        f"--workpath={build_dir}", # Ruta para archivos temporales de compilación
        f"--specpath={release_dir}" # Ruta para el archivo .spec
    ]

    try:
        subprocess.run(pyinstaller_command, check=True)
        print("PyInstaller completado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la ejecución de PyInstaller: {e}")
        sys.exit(1)

    # Crear un archivo ZIP con el ejecutable y los assets
    zip_filename = os.path.join(release_dir, f"PyGame_v{version}.zip")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Añadir el ejecutable
        exe_name = f"PyGame_v{version}.exe" if sys.platform == "win32" else f"PyGame_v{version}"
        exe_path = os.path.join(dist_dir, exe_name)
        if os.path.exists(exe_path):
            zipf.write(exe_path, os.path.basename(exe_path))
        else:
            print(f"Advertencia: El ejecutable {exe_path} no se encontró para el archivo ZIP.")

        # Añadir la carpeta assets
        for root, _, files in os.walk("assets"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, os.path.dirname("assets")))
        
        print(f"Archivo ZIP creado: {zip_filename}")

    # Limpiar archivos de compilación de PyInstaller
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    spec_file = os.path.join(release_dir, f"PyGame_v{version}.spec")
    if os.path.exists(spec_file):
        os.remove(spec_file)
    
    print("Proceso de empaquetado completado.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tools/package.py [major|minor|patch]")
        sys.exit(1)

    version_type = sys.argv[1]
    new_version = update_version(version_type)
    package_project(new_version)