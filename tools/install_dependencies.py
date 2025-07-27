import subprocess
import sys

def install_pygame():
    try:
        import pygame
    except ImportError:
        print("Pygame not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

if __name__ == "__main__":
    install_pygame()
