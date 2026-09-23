import io
import os
import subprocess

from PIL import Image
import numpy as np
import easyocr

from core.translator import Translator


class WindowTranslator:
    def __init__(self, root):
        self.root = root
        self.overlay = None
        self.reader = None
        self.translator = None
        self.win_id = None
        self.window_name = ""

        self.crop_top = 80
        self.overlay_visible = False

        # кеш перекладів
        self.cache = {}

        self.debug = False
        os.makedirs("screenshots", exist_ok=True)

        print("⏳ Завантаження OCR...")
        self.reader = easyocr.Reader(["ja", "en"], gpu=False)

        print("⏳ Завантаження перекладача...")
        self.translator = Translator()

        self.src_lang = "en"
        self.dst_lang = "uk"

        self.bind_hotkey()
        print("✅ WindowTranslator готовий")

    def bind_hotkey(self):
        self.root.bind("<Control-space>", lambda e: self.toggle_translation())

    def set_overlay(self, overlay):
        self.overlay = overlay

    def toggle_translation(self):
        if self.overlay_visible:
            self.hide_translation()
            return

        try:
            self.win_id = subprocess.check_output(
                ["xdotool", "selectwindow"]
            ).decode().strip()
        except Exception as e:
            print("❌ Не вдалося вибрати вікно:", e)
            return

        print("✅ Вікно:", self.win_id)
        self.translate_window()

    def capture_window(self):
        proc = subprocess.Popen(
            ["xwd", "-id", self.win_id, "-silent"],
            stdout=subprocess.PIPE
        )
        png = subprocess.check_output(
            ["convert", "xwd:-", "png:-"],
            stdin=proc.stdout
        )
        proc.wait()

        img = Image.open(io.BytesIO(png)).convert("RGB")
        img = img.crop((0, self.crop_top, img.width, img.height))

        if self.debug:
            img.save("screenshots/original.png")

        return img

    def detect_text(self, img):
        frame = np.array(img)
        return self.reader.readtext(
            frame,
            paragraph=False,
            min_size=12,
            text_threshold=0.7,
            low_text=0.4
        )

    def translate_text(self, text):
        key = f"{self.src_lang}|{self.dst_lang}|{text}"
        if key in self.cache:
            return self.cache[key]
        try:
            translated = self.translator.translate(text, source=self.src_lang, target=self.dst_lang)
            self.cache[key] = translated
            return translated
        except Exception as e:
            print("❌ Помилка перекладу:", e)
            return ""

    def translate_window(self):
        img = self.capture_window()
        results = self.detect_text(img)

        if self.overlay:
            self.overlay.clear()

        found = False
        for item in results:
            box, text, confidence = item[0], item[1], item[2]

            if confidence < 0.45 or len(text.strip()) < 2:
                continue

            translation = self.translate_text(text)
            if not translation:
                continue

            found = True
            print("🔎 OCR:", text)
            print("🇺🇦:", translation)
            print("----------------")

            x = int((box[0][0] + box[1][0]) / 2)
            y = int((box[0][1] + box[2][1]) / 2) + self.crop_top

            if self.overlay:
                self.overlay.show_translation(x, y, translation)

        if found:
            self.overlay_visible = True
            print("✅ Переклад показано")
        else:
            print("⚠️ Текст не знайдено")
            if self.overlay:
                self.overlay.clear()
                self.overlay.hide()
            self.overlay_visible = False

    def hide_translation(self):
        if self.overlay:
            self.overlay.clear()
            self.overlay.hide()
        self.overlay_visible = False
        print("⛔ Переклад приховано")

    def clear_cache(self):
        self.cache = {}

    def stop(self):
        self.hide_translation()
        self.clear_cache()
        self.win_id = None

    def is_overlay_visible(self):
        return self.overlay_visible

    def set_languages(self, src, dst):
        self.src_lang = src
        self.dst_lang = dst
        print(f"🌍 Мови перекладу оновлено: {src} → {dst}")

    def reload_languages(self):
        try:
            self.translator = Translator()
            print("🔄 Список мов оновлено")
        except Exception as e:
            print("❌ Не вдалося оновити мови:", e)
