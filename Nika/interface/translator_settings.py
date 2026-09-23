import customtkinter as ctk
import argostranslate.package


class TranslatorSettings(ctk.CTkToplevel):
    def __init__(self, parent, translator):
        super().__init__(parent)

        self.translator = translator
        self.title("Налаштування перекладача")
        self.geometry("360x380")
        self.configure(fg_color="#202225")

        # Мова оригіналу
        self.src_var = ctk.StringVar(value="auto")
        ctk.CTkLabel(self, text="Мова оригіналу").pack()
        self.src_menu = ctk.CTkOptionMenu(
            self,
            values=["auto", "uk", "en", "de", "fr", "ru", "es", "it", "pl", "zh", "ja"],
            variable=self.src_var
        )
        self.src_menu.pack(pady=8)

        # Мова перекладу
        self.dst_var = ctk.StringVar(value="uk")
        ctk.CTkLabel(self, text="Мова перекладу").pack()
        self.dst_menu = ctk.CTkOptionMenu(
            self,
            values=["uk", "en", "de", "fr", "ru", "es", "it", "pl", "zh", "ja"],
            variable=self.dst_var
        )
        self.dst_menu.pack(pady=8)

        # Поле для додавання нової мови
        ctk.CTkLabel(self, text="Додати нову мову (ISO‑код)").pack(pady=(10, 0))
        self.new_lang_entry = ctk.CTkEntry(self, placeholder_text="наприклад: pt")
        self.new_lang_entry.pack(pady=5)

        add_btn = ctk.CTkButton(
            self,
            text="➕ Додати мову",
            fg_color="#5865F2",
            hover_color="#7289DA",
            command=self.add_language
        )
        add_btn.pack(pady=5)

        # Повідомлення про статус
        self.status_label = ctk.CTkLabel(self, text="", text_color="white")
        self.status_label.pack(pady=5)

        # Кнопка збереження
        ctk.CTkButton(
            self,
            text="Зберегти",
            fg_color="#5865F2",
            hover_color="#7289DA",
            command=self.save_settings
        ).pack(pady=15)

    def add_language(self):
        new_lang = self.new_lang_entry.get().strip()
        if not new_lang:
            self.status_label.configure(text="⚠️ Введіть код мови", text_color="#FFAA00")
            return

        try:
            available_packages = argostranslate.package.get_available_packages()

            # шукаємо пакет для src -> new_lang
            package_to_install = next(
                (p for p in available_packages if p.from_code == self.src_var.get() and p.to_code == new_lang),
                None
            )

            if package_to_install:
                argostranslate.package.install_from_path(package_to_install.download())
                self.translator.reload_languages()
                self.status_label.configure(
                    text=f"✅ Пакет для {self.src_var.get()} → {new_lang} встановлено",
                    text_color="#57F287"
                )

                if new_lang not in self.src_menu._values:
                    self.src_menu.configure(values=self.src_menu._values + [new_lang])
                    self.dst_menu.configure(values=self.dst_menu._values + [new_lang])

            else:
                self.status_label.configure(
                    text=f"⚠️ Пакет {self.src_var.get()} → {new_lang} не знайдено",
                    text_color="#FFAA00"
                )

            self.new_lang_entry.delete(0, "end")

        except Exception as e:
            self.status_label.configure(text=f"❌ Помилка: {e}", text_color="#FF5555")

    def save_settings(self):
        src = self.src_var.get()
        dst = self.dst_var.get()
        self.translator.set_languages(src, dst)
        self.destroy()
