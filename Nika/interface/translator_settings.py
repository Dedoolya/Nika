import customtkinter as ctk
import argostranslate.package


LANGUAGES = [
    "uk",
    "en",
    "de",
    "fr",
    "ru",
    "es",
    "it",
    "pl",
    "zh",
    "ja",
]


class TranslatorSettings(ctk.CTkToplevel):
    def __init__(self, parent, translator):
        super().__init__(parent)

        self.translator = translator
        self.title("Налаштування перекладача")
        self.geometry("360x380")
        self.configure(fg_color="#202225")
        self.transient(parent)

        self.src_var = ctk.StringVar(value=translator.src_lang)
        ctk.CTkLabel(self, text="Мова оригіналу").pack()

        self.src_menu = ctk.CTkOptionMenu(
            self,
            values=["auto"] + LANGUAGES,
            variable=self.src_var,
        )
        self.src_menu.pack(pady=8)

        self.dst_var = ctk.StringVar(value=translator.dst_lang)
        ctk.CTkLabel(self, text="Мова перекладу").pack()

        self.dst_menu = ctk.CTkOptionMenu(
            self,
            values=LANGUAGES,
            variable=self.dst_var,
        )
        self.dst_menu.pack(pady=8)

        ctk.CTkLabel(
            self,
            text="Додати мову (ISO-код)",
        ).pack(pady=(10, 0))

        self.new_lang_entry = ctk.CTkEntry(
            self,
            placeholder_text="наприклад: pt",
        )
        self.new_lang_entry.pack(pady=5)

        ctk.CTkButton(
            self,
            text="➕ Додати мову",
            fg_color="#5865F2",
            hover_color="#7289DA",
            command=self.add_language,
        ).pack(pady=5)

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            text_color="white",
            wraplength=320,
        )
        self.status_label.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Зберегти",
            fg_color="#5865F2",
            hover_color="#7289DA",
            command=self.save_settings,
        ).pack(pady=15)

    def _add_language_to_menus(self, code):
        src_values = list(self.src_menu._values)
        dst_values = list(self.dst_menu._values)

        if code not in src_values:
            self.src_menu.configure(values=src_values + [code])

        if code not in dst_values:
            self.dst_menu.configure(values=dst_values + [code])

    def add_language(self):
        new_lang = self.new_lang_entry.get().strip().lower()

        if not new_lang or len(new_lang) < 2:
            self.status_label.configure(
                text="⚠️ Введіть коректний ISO-код",
                text_color="#FFAA00",
            )
            return

        if new_lang == "auto":
            self.status_label.configure(
                text="⚠️ auto не є мовним пакетом",
                text_color="#FFAA00",
            )
            return

        try:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()

            source = self.src_var.get()

            if source == "auto":
                source = "en"

            installed = []
            for from_code, to_code in (
                (source, new_lang),
                (new_lang, source),
            ):
                if from_code == to_code:
                    continue

                package = next(
                    (
                        p for p in available_packages
                        if p.from_code == from_code
                        and p.to_code == to_code
                    ),
                    None,
                )

                if package is None:
                    continue

                try:
                    argostranslate.package.install_from_path(
                        package.download()
                    )
                    installed.append(f"{from_code} → {to_code}")
                except Exception as error:
                    print(f"⚠️ Не вдалося встановити {from_code} → {to_code}: {error}")

            self.translator.reload_languages()

            if installed:
                self._add_language_to_menus(new_lang)
                self.status_label.configure(
                    text="✅ Встановлено: " + ", ".join(installed),
                    text_color="#57F287",
                )
            else:
                self.status_label.configure(
                    text=f"⚠️ Пакети для {source} ↔ {new_lang} не знайдено",
                    text_color="#FFAA00",
                )

        except Exception as error:
            self.status_label.configure(
                text=f"❌ Не вдалося додати мову: {error}",
                text_color="#FF5555",
            )
        finally:
            self.new_lang_entry.delete(0, "end")

    def save_settings(self):
        src = self.src_var.get()
        dst = self.dst_var.get()

        if src == dst and src != "auto":
            self.status_label.configure(
                text="⚠️ Мова оригіналу та перекладу однакова",
                text_color="#FFAA00",
            )
            return

        self.translator.set_languages(src, dst)
        self.destroy()
