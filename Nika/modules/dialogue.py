import json
import os
import random

from rapidfuzz import fuzz

from core.paths import DATA_DIR, BASE_DIR


class Dialogue:
    def __init__(self, config_path=None, data_path=None):
        self.dialogs = []
        self.fallback = None

        config_path = config_path or os.path.join(DATA_DIR, "config.json")
        data_path = data_path or DATA_DIR

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Не знайдено конфіг: {config_path}")

        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        sources = config.get("dialogue_sources", [])
        self.fallback = config.get("fallback")

        for filename in sources:
            file_path = os.path.join(data_path, filename)

            if not os.path.exists(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            dialogs = data.get("dialogs", [])
            if isinstance(dialogs, list):
                self.dialogs.extend(
                    dialog for dialog in dialogs if isinstance(dialog, dict)
                )

    def get_response(self, user_message):
        msg = user_message.lower().strip()

        for dialog in self.dialogs:
            for pattern in dialog.get("patterns", []):
                if not isinstance(pattern, str):
                    continue

                score = fuzz.ratio(pattern.lower(), msg)

                if score >= 80:
                    responses = dialog.get("responses", [])
                    if responses:
                        return random.choice(responses)

        if self.fallback:
            fallback_path = os.path.join(DATA_DIR, self.fallback)

            if os.path.exists(fallback_path):
                with open(fallback_path, "r", encoding="utf-8") as file:
                    fallback_data = json.load(file)

                for dialog in fallback_data.get("dialogs", []):
                    responses = dialog.get("responses", [])

                    if isinstance(responses, list) and responses:
                        return random.choice(responses)

        return f"Я почула: '{user_message}'. Хочу зрозуміти тебе краще 💖"
