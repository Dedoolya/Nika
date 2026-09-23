import json
import os

from core.paths import DATA_DIR


class Memory:
    def __init__(
        self,
        log_path=None,
        config_path=None,
    ):
        self.history = []
        self.log_path = log_path or os.path.join(DATA_DIR, "messages.log")
        self.config_path = config_path or os.path.join(DATA_DIR, "config.json")

        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        if not os.path.exists(self.log_path):
            open(self.log_path, "a", encoding="utf-8").close()

        self.context_size = 5

        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as file:
                config = json.load(file)

            self.context_size = config.get("context_size", 5)

        self._load_history()

    def _load_history(self):
        try:
            with open(self.log_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.rstrip("\n")

                    if ": " not in line:
                        continue

                    role, message = line.split(": ", 1)
                    self.history.append((role, message))

        except OSError:
            self.history = []

    def save(self, role, message):
        self.history.append((role, message))

        with open(self.log_path, "a", encoding="utf-8") as file:
            file.write(f"{role}: {message}\n")

    def get_context(self):
        return self.history[-self.context_size:]

    def get_all(self):
        return self.history
