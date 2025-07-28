#!/usr/bin/env python3
"""
Gestor de guardado y carga de partidas para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Sistema de guardado/carga de partidas con soporte para múltiples slots y logging avanzado.
"""
import json
import os
from utils.advanced_logger import get_logger

class SaveManager:
    def __init__(self, logger=None):
        self.logger = logger or get_logger("PyGame")
        self.save_dir = "saves"
        os.makedirs(self.save_dir, exist_ok=True)
        self.logger.log_event(f"SaveManager inicializado - Directorio: {self.save_dir}", "save")

    def _get_save_path(self, slot):
        return os.path.join(self.save_dir, f"save_slot_{slot}.json")

    def save_game(self, slot, game_state):
        path = self._get_save_path(slot)
        try:
            with open(path, "w") as f:
                json.dump(game_state, f, indent=4)
            self.logger.log_event(f"Juego guardado en el slot {slot}", "save")
            return True
        except Exception as e:
            self.logger.log_error(f"Error al guardar en el slot {slot}: {e}", "save", exc_info=True)
            return False

    def load_game(self, slot):
        path = self._get_save_path(slot)
        if not os.path.exists(path):
            self.logger.log_warning(f"No hay datos guardados en el slot {slot}", "save")
            return None
        try:
            with open(path, "r") as f:
                game_state = json.load(f)
            self.logger.log_event(f"Juego cargado del slot {slot}", "save")
            return game_state
        except Exception as e:
            self.logger.log_error(f"Error al cargar del slot {slot}: {e}", "save", exc_info=True)
            return None

    def get_save_slots_status(self):
        statuses = {}
        for i in range(1, 4): # 3 slots
            path = self._get_save_path(i)
            statuses[i] = os.path.exists(path)
        self.logger.log_debug(f"Estado de slots: {statuses}", "save")
        return statuses

    def get_save_slots(self):
        """Obtiene información detallada de todos los slots de guardado."""
        slots = {}
        for i in range(1, 4):  # 3 slots
            path = self._get_save_path(i)
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        save_data = json.load(f)
                    slots[i] = save_data
                except Exception as e:
                    self.logger.log_error(f"Error leyendo slot {i}: {e}", "save", exc_info=True)
                    slots[i] = {}
            else:
                slots[i] = {}  # Slot vacío
        
        self.logger.log_event(f"Slots de guardado obtenidos: {len(slots)}", "save")
        
        return slots
