import json
import os

class SaveManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.save_dir = "saves"
        os.makedirs(self.save_dir, exist_ok=True)

    def _get_save_path(self, slot):
        return os.path.join(self.save_dir, f"save_slot_{slot}.json")

    def save_game(self, slot, game_state):
        path = self._get_save_path(slot)
        try:
            with open(path, "w") as f:
                json.dump(game_state, f, indent=4)
            if self.logger:
                self.logger.log_event(f"Juego guardado en el slot {slot}.")
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error al guardar en el slot {slot}: {e}")
            return False

    def load_game(self, slot):
        path = self._get_save_path(slot)
        if not os.path.exists(path):
            if self.logger:
                self.logger.log_event(f"No hay datos guardados en el slot {slot}.")
            return None
        try:
            with open(path, "r") as f:
                game_state = json.load(f)
            if self.logger:
                self.logger.log_event(f"Juego cargado del slot {slot}.")
            return game_state
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error al cargar del slot {slot}: {e}")
            return None

    def get_save_slots_status(self):
        statuses = {}
        for i in range(1, 4): # 3 slots
            path = self._get_save_path(i)
            statuses[i] = os.path.exists(path)
        return statuses
