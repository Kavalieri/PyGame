from managers.save_manager import SaveManager
from managers.logger import Logger
from ui.menus.base_menu import BaseMenu
from ui.menus.character_selection_menu import CharacterSelectionMenu

class Menu(BaseMenu):
    def __init__(self, screen, save_manager: SaveManager, logger: Logger, game_loop):
        self.save_manager = save_manager
        self.game_loop = game_loop
        
        main_menu_options = [
            {"text": "Nueva Partida", "action": "new_game"},
            {"text": "Cargar Partida", "action": "load_game"},
            {"text": "Guardar Juego", "action": "save_game"},
            {"text": "Salir", "action": "exit"}
        ]
        super().__init__(screen, logger, title_text="Juego Modularizado", options=main_menu_options,
                         background_image_path="assets/images/fondos/parque.jpg",
                         button_images={
                             'normal': "assets/images/ui/Buttons/Blue/Blank 1.png",
                             'hover': "assets/images/ui/Buttons/Blue/Blank 2.png"
                         })

    def show(self, message=None):
        return self.show_main_menu()

    def show_main_menu(self):
        self.logger.log_debug("Mostrando menú principal.")
        while True:
            action = self._handle_input()
            if action == "save_game":
                self.show_save_menu()
                return "continue"
            elif action:
                return action
            self._draw()

    def show_save_menu(self):
        slots_status = self.save_manager.get_save_slots_status()
        options_data = []
        for i in range(1, 4):
            status = "(Ocupado)" if slots_status[i] else "(Vacío)"
            options_data.append({"text": f"Slot {i} {status}", "action": f"save_slot_{i}"})
        options_data.append({"text": "Volver", "action": "back"})

        save_menu_instance = BaseMenu(self.screen, self.logger, title_text="Guardar Juego", options=options_data,
                                      background_image_path="assets/images/fondos/game_background_1_dark.png",
                                      button_images={
                                          'normal': "assets/images/ui/Buttons/Blue/Blank 1.png",
                                          'hover': "assets/images/ui/Buttons/Blue/Blank 2.png"
                                      })
        
        while True:
            action = save_menu_instance.show()
            if action == "back":
                return
            elif action.startswith("save_slot_"):
                slot_number = int(action.split("_")[2])
                self.logger.log_event(f"Intentando guardar en el slot {slot_number}")
                game_state = self.game_loop.get_game_state()
                self.save_manager.save_game(slot_number, game_state)
                return

    def show_load_menu(self):
        slots_status = self.save_manager.get_save_slots_status()
        options_data = []
        for i in range(1, 4):
            status = "(Ocupado)" if slots_status[i] else "(Vacío)"
            options_data.append({"text": f"Slot {i} {status}", "action": f"load_slot_{i}"})
        options_data.append({"text": "Volver", "action": "back"})

        load_menu_instance = BaseMenu(self.screen, self.logger, title_text="Cargar Juego", options=options_data,
                                      background_image_path="assets/images/fondos/game_background_1_dark.png",
                                      button_images={
                                          'normal': "assets/images/ui/Buttons/Blue/Blank 1.png",
                                          'hover': "assets/images/ui/Buttons/Blue/Blank 2.png"
                                      })

        while True:
            action = load_menu_instance.show()
            if action == "back":
                return None
            elif action.startswith("load_slot_"):
                slot_number = int(action.split("_")[2])
                self.logger.log_event(f"Intentando cargar del slot {slot_number}")
                loaded_state = self.save_manager.load_game(slot_number)
                return loaded_state

    def show_new_game_save_slot_selection(self):
        slots_status = self.save_manager.get_save_slots_status()
        options_data = []
        for i in range(1, 4):
            status = "(Ocupado)" if slots_status[i] else "(Vacío)"
            options_data.append({"text": f"Slot {i} {status}", "action": f"select_slot_{i}"})
        options_data.append({"text": "Volver", "action": "back"})

        new_game_slot_menu_instance = BaseMenu(self.screen, self.logger, title_text="Selecciona Slot para Nueva Partida", options=options_data,
                                               background_image_path="assets/images/fondos/game_background_1_dark.png",
                                               button_images={
                                                   'normal': "assets/images/ui/Buttons/Blue/Blank 1.png",
                                                   'hover': "assets/images/ui/Buttons/Blue/Blank 2.png"
                                               })

        while True:
            action = new_game_slot_menu_instance.show()
            if action == "back":
                return None
            elif action.startswith("select_slot_"):
                slot_number = int(action.split("_")[2])
                return slot_number

    def show_character_selection_menu(self):
        character_selection_menu = CharacterSelectionMenu(self.screen, self.logger)
        return character_selection_menu.show()

    def show_game_over(self, final_score):
        """Muestra la pantalla de fin de juego con la puntuación final."""
        self.logger.log_event(f"Juego terminado. Puntuación final: {final_score}")
        
        game_over_options = [
            {"text": "Nueva Partida", "action": "new_game"},
            {"text": "Volver al Menú Principal", "action": "main_menu"},
            {"text": "Salir", "action": "exit"}
        ]
        
        game_over_menu = BaseMenu(self.screen, self.logger, 
                                 title_text=f"¡Juego Terminado! Puntuación: {final_score}", 
                                 options=game_over_options,
                                 background_image_path="assets/images/fondos/game_background_1_dark.png",
                                 button_images={
                                     'normal': "assets/images/ui/Buttons/Blue/Blank 1.png",
                                     'hover': "assets/images/ui/Buttons/Blue/Blank 2.png"
                                 })
        
        return game_over_menu.show()
