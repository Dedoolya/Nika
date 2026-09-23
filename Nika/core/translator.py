import argostranslate.translate
from core.translate_cache import TranslationCache


class Translator:
    def __init__(self):
        self.reload_languages()
        self.cache = TranslationCache()

    def reload_languages(self):
        self.languages = argostranslate.translate.get_installed_languages()

    def translate(self, text, source="en", target="uk"):
        # 1. Формуємо ключ для кешу
        cached = self.cache.get(source, target, text)
        if cached is not None:
            print("⚡ Переклад із кешу")
            return cached

        translated = ""
        try:
            # 2. Пробуємо прямий переклад
            translated = argostranslate.translate.translate(text, source, target)

            # 3. Якщо результат порожній або дивний — пробуємо через англійську
            if (not translated.strip()) and source != "en":
                mid = argostranslate.translate.translate(text, source, "en")
                translated = argostranslate.translate.translate(mid, "en", target)

        except Exception as e:
            print("❌ Помилка перекладу:", e)
            # fallback через англійську
            if source != "en":
                try:
                    mid = argostranslate.translate.translate(text, source, "en")
                    translated = argostranslate.translate.translate(mid, "en", target)
                except Exception as e2:
                    print("❌ Fallback теж не спрацював:", e2)
                    translated = text  # повертаємо оригінал
            else:
                translated = text

        # 4. Записуємо у кеш
        self.cache.add(source, target, text, translated)

        return translated
