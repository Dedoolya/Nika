import os
import json

class Memory:
    def __init__(self, log_path="data/messages.log", config_path="data/config.json"):
        self.history = []
        self.log_path = log_path
        self.config_path = config_path

        # створюємо файл якщо його немає
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        if not os.path.exists(log_path):
            open(log_path, "w").close()

        # завантажуємо налаштування
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.context_size = config.get("context_size", 5)
        else:
            self.context_size = 5

    def save(self, role, message):
        self.history.append((role, message))
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"{role}: {message}\n")

    def get_context(self):
        return self.history[-self.context_size:]

    def get_all(self):
        return self.history

