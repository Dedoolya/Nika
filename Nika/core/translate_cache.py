import json
import os

from core.paths import DATA_DIR


class TranslationCache:
    def __init__(self):
        self.cache_file = os.path.join(DATA_DIR, "translate_cache.json")
        os.makedirs(DATA_DIR, exist_ok=True)

        if not os.path.exists(self.cache_file):
            with open(self.cache_file, "w", encoding="utf-8") as file:
                json.dump({}, file, ensure_ascii=False, indent=4)

    def load(self):
        try:
            with open(self.cache_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def save(self, cache):
        with open(self.cache_file, "w", encoding="utf-8") as file:
            json.dump(cache, file, ensure_ascii=False, indent=4)

    def get(self, source, target, text):
        cache = self.load()
        key = f"{source}|{target}|{text}"
        return cache.get(key)

    def add(self, source, target, text, translation):
        cache = self.load()
        key = f"{source}|{target}|{text}"
        cache[key] = translation
        self.save(cache)
