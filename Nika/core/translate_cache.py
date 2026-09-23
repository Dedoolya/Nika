import json
import os


class TranslationCache:

    def __init__(self):
        self.cache_file = "data/translate_cache.json"

        if not os.path.exists(self.cache_file):
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def load(self):
        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, cache):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)

    def get(self, source, target, text):
        """Повертає переклад із кешу або None."""

        cache = self.load()

        key = f"{source}|{target}|{text}"

        return cache.get(key)

    def add(self, source, target, text, translation):
        """Додає новий переклад у кеш."""

        cache = self.load()

        key = f"{source}|{target}|{text}"

        cache[key] = translation

        self.save(cache)