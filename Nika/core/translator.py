import re

import argostranslate.translate

from core.translate_cache import TranslationCache


class Translator:
    def __init__(self):
        self.languages = []
        self.cache = TranslationCache()
        self.reload_languages()

    def reload_languages(self):
        self.languages = argostranslate.translate.get_installed_languages()

    def _installed_codes(self):
        return {language.code for language in self.languages}

    def _detect_source_language(self, text):
        """Просте офлайн-визначення мови для режиму auto."""
        installed = self._installed_codes()

        if re.search(r"[іїєґІЇЄҐ]", text) and "uk" in installed:
            return "uk"

        if re.search(r"[ыэъёЫЭЪЁ]", text) and "ru" in installed:
            return "ru"

        if re.search(r"[а-яА-Я]", text):
            if "uk" in installed:
                return "uk"
            if "ru" in installed:
                return "ru"

        if "en" in installed:
            return "en"

        return None

    def translate(self, text, source="en", target="uk"):
        text = text.strip()

        if not text:
            return ""

        if source == target:
            return text

        if source == "auto":
            detected = self._detect_source_language(text)

            if detected is None:
                print("⚠️ Не вдалося визначити мову тексту")
                return text

            source = detected

        installed = self._installed_codes()

        if source not in installed:
            raise ValueError(f"Мова джерела {source} не встановлена")

        if target not in installed:
            raise ValueError(f"Мова перекладу {target} не встановлена")

        cached = self.cache.get(source, target, text)
        if cached is not None:
            print("⚡ Переклад із кешу")
            return cached

        try:
            translated = argostranslate.translate.translate(
                text,
                source,
                target,
            )
        except Exception as error:
            print(f"❌ Помилка перекладу {source} → {target}: {error}")
            return text

        if not translated or not translated.strip():
            return text

        self.cache.add(source, target, text, translated)
        return translated
