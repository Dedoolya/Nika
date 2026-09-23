import random
import json
import os
from rapidfuzz import fuzz  # ✅ додаємо бібліотеку для нечіткого порівняння

class Dialogue:
    def __init__(self, config_path="data/config.json", data_path="data"):
        self.dialogs = []
        self.fallback = None

        # завантажуємо конфіг
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                sources = config.get("dialogue_sources", [])
                self.fallback = config.get("fallback")

                # завантажуємо всі файли зі списку
                for filename in sources:
                    file_path = os.path.join(data_path, filename)
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f_json:
                            data = json.load(f_json)
                            if "dialogs" in data and isinstance(data["dialogs"], list):
                                for d in data["dialogs"]:
                                    if isinstance(d, dict):
                                        self.dialogs.append(d)

    def get_response(self, user_message):
        msg = user_message.lower()

        # перевіряємо всі діалоги з нечітким порівнянням
        for dialog in self.dialogs:
            if isinstance(dialog, dict):
                for pattern in dialog.get("patterns", []):
                    score = fuzz.ratio(pattern.lower(), msg)  # порівняння схожості
                    if score >= 80:  # ✅ поріг схожості (можна змінити)
                        responses = dialog.get("responses", [])
                        if responses:
                            return random.choice(responses)

        # fallback
        if self.fallback:
            fb_path = os.path.join("data", self.fallback)
            if os.path.exists(fb_path):
                with open(fb_path, "r", encoding="utf-8") as f:
                    fb_data = json.load(f)
                    if "dialogs" in fb_data and isinstance(fb_data["dialogs"], list):
                        fb_dialogs = fb_data["dialogs"]
                        if fb_dialogs and isinstance(fb_dialogs[0], dict):
                            responses = fb_dialogs[0].get("responses", [])
                            if responses:
                                return random.choice(responses)

        return f"Я почула: '{user_message}'. Хочу зрозуміти тебе краще 💖"
