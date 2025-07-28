import shutil
import os

def copiar_archivos(origen, destino, archivos):
    if not os.path.exists(destino):
        os.makedirs(destino)
    for archivo in archivos:
        try:
            ruta_origen = os.path.join(origen, archivo)
            ruta_destino = os.path.join(destino, archivo)
            shutil.copy(ruta_origen, ruta_destino)
            if not os.path.exists(ruta_destino):
                print(f"Error: El archivo {archivo} no se copió correctamente.")
            else:
                print(f"Archivo copiado correctamente: {archivo}")
        except Exception as e:
            print(f"Error al copiar {archivo}: {e}")

# Ejemplo de uso
# Directorios
# origen = r'c:\ruta\de\origen'
# destino = r'c:\ruta\de\destino'
# archivos = [
#     'archivo1.png',
#     'archivo2.mp4',
#     'script.py'
# ]

# copiar_archivos(origen, destino, archivos)
