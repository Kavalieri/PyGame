import os

class Logger:
    def __init__(self, log_file='logs/log.txt'):
        self.log_file = log_file
        if not os.path.exists('logs'):
            os.makedirs('logs')

    def log(self, message):
        with open(self.log_file, 'a') as file:
            file.write(f"{message}\n")

    def log_event(self, event):
        self.log(f"EVENT: {event}")

    def log_error(self, error):
        self.log(f"ERROR: {error}")

    def log_warning(self, warning_message):
        self.log(f"WARNING: {warning_message}")

    def log_debug(self, debug_message):
        self.log(f"DEBUG: {debug_message}")
