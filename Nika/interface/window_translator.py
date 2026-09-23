import io
import os
import shutil
import subprocess

from PIL import Image
import numpy as np

from core.paths import SCREENSHOTS_DIR
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
        self.cache = {}
        self.debug = False

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

        self.src_lang = "en"
        self.dst_lang = "uk"

        self.bind_hotkey()
        print("✅ WindowTranslator готовий")

    def _ensure_ocr(self):
        if self.reader is not None:
            return True

        try:
            import easyocr
            print("⏳ Завантаження OCR...")
            self.reader = easyocr.Reader(["ja", "en"], gpu=False)
            print("✅ OCR готовий")
            return True
        except Exception as error:
            print(f"❌ Не вдалося завантажити OCR: {error}")
            return False

    def bind_hotkey(self):
        self.root.bind(
            "<Control-space>",
            lambda event: self.toggle_translation()
        )

    def set_overlay(self, overlay):
        self.overlay = overlay

    def toggle_translation(self):
        if self.overlay_visible:
            self.hide_translation()
            return

        if not self._check_system_tools():
            return

        try:
            self.win_id = subprocess.check_output(
                ["xdotool", "selectwindow"],
                text=True,
            ).strip()
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            print(f"❌ Не вдалося вибрати вікно: {error}")
            return

        print("✅ Вікно:", self.win_id)
        self.translate_window()

    def _check_system_tools(self):
        missing = [
            tool
            for tool in ("xdotool", "xwd", "convert")
            if shutil.which(tool) is None
        ]

        if missing:
            print(
                "❌ Для перекладача не вистачає системних утиліт: "
                + ", ".join(missing)
            )
            return False

        return True

    def capture_window(self):
        proc = subprocess.Popen(
            ["xwd", "-id", self.win_id, "-silent"],
            stdout=subprocess.PIPE,
        )

        try:
            png = subprocess.check_output(
                ["convert", "xwd:-", "png:-"],
                stdin=proc.stdout,
            )
        finally:
            if proc.stdout:
                proc.stdout.close()
            proc.wait()

        img = Image.open(io.BytesIO(png)).convert("RGB")
        img = img.crop((0, self.crop_top, img.width, img.height))

        if self.debug:
            img.save(os.path.join(SCREENSHOTS_DIR, "original.png"))

        return img

    def detect_text(self, img):
        if not self._ensure_ocr():
            return []

        frame = np.array(img)

        return self.reader.readtext(
            frame,
            paragraph=False,
            min_size=12,
            text_threshold=0.7,
            low_text=0.4,
        )

    def translate_text(self, text):
        key = f"{self.src_lang}|{self.dst_lang}|{text}"

        if key in self.cache:
            return self.cache[key]

        try:
            if self.translator is None:
                self.translator = Translator()

            translated = self.translator.translate(
                text,
                source=self.src_lang,
                target=self.dst_lang,
            )
            self.cache[key] = translated
            return translated
        except Exception as error:
            print(f"❌ Помилка перекладу: {error}")
            return ""

    def translate_window(self):
        try:
            img = self.capture_window()
            results = self.detect_text(img)
        except Exception as error:
            print(f"❌ Помилка захоплення/OCR: {error}")
            return

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
        except Exception as error:
            print(f"❌ Не вдалося оновити мови: {error}")
