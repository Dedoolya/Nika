import customtkinter as ctk
from interface.translator_settings import TranslatorSettings


class AvatarMenu(ctk.CTkFrame):

    def __init__(self, parent, window_translator):
        super().__init__(
            parent,
            width=185,
            height=120,
            fg_color="#202225",
            corner_radius=12,
            border_width=1,
            border_color="#313338"
        )

        self.pack_propagate(False)
        self.window_translator = window_translator

        # ==========================
        # Кнопки
        # ==========================
        self.create_item("🌍", "Перекладач", command=self.open_translator_settings)
        self.create_item("⚙️", "Налаштування")
        self.create_item("ℹ️", "Про Ніку")

    def create_item(self, icon, text, command=None):
        button = ctk.CTkButton(
            self,
            text=f"{icon}   {text}",
            height=34,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#2b2d31",
            anchor="w",
            text_color="white",
            font=("Segoe UI", 13),
            command=command if command else lambda t=text: print(t)
        )
        button.pack(fill="x", padx=8, pady=2)

    def open_translator_settings(self):
        TranslatorSettings(self.master, self.window_translator)
