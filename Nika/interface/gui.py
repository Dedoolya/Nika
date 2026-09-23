import os
from datetime import datetime

import customtkinter as ctk
from PIL import Image, ImageDraw

from core.chat import ChatBot
from core.paths import BASE_DIR
from interface.avatar_menu import AvatarMenu
from interface.overlay import Overlay
from interface.window_translator import WindowTranslator


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def make_circle_avatar(path, size=(50, 50)):
    img = Image.open(path).resize(size).convert("RGBA")

    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    img.putalpha(mask)
    return img


class ChatGUI:
    def __init__(self, root):
        self.root = root

        self.chatbot = ChatBot()
        self.overlay = Overlay(self.root)
        self.window_translator = WindowTranslator(self.root)
        self.window_translator.set_overlay(self.overlay)

        self.last_activity = datetime.now()
        self.avatar_menu = None

        self.root.title("Ніка")
        self.root.geometry("450x200")
        self.root.minsize(400, 150)
        self.root.configure(fg_color="#18191c")

        self.header = ctk.CTkFrame(
            self.root, height=60, corner_radius=0, fg_color="#202225"
        )
        self.header.pack(fill="x")

        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=0)

        self.title = ctk.CTkLabel(
            self.header,
            text="💜 Ніка",
            font=("Segoe UI", 22, "bold"),
        )
        self.title.grid(row=0, column=0, sticky="w", padx=15, pady=(8, 0))

        self.status = ctk.CTkLabel(
            self.header,
            text="🟢 Онлайн",
            font=("Segoe UI", 12),
            text_color="#57F287",
        )
        self.status.grid(row=1, column=0, sticky="w", padx=18)

        avatar_path = os.path.join(BASE_DIR, "interface", "avatar.jpg")

        try:
            image = make_circle_avatar(avatar_path, (50, 50))
            self.avatar_img = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(50, 50),
            )
            self.avatar_button = ctk.CTkButton(
                self.header,
                image=self.avatar_img,
                text="",
                width=54,
                height=54,
                corner_radius=27,
                fg_color="transparent",
                hover_color="#2b2d31",
                command=self.toggle_avatar_menu,
            )
        except Exception as error:
            print(f"⚠️ Не вдалося завантажити аватар: {error}")
            self.avatar_button = ctk.CTkButton(
                self.header,
                text="👩",
                font=("Segoe UI Emoji", 32),
                width=54,
                height=54,
                corner_radius=27,
                fg_color="transparent",
                hover_color="#2b2d31",
                command=self.toggle_avatar_menu,
            )

        self.avatar_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=10,
            pady=10,
        )

        self.main = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main.pack(fill="both", expand=True)

        self.response = ctk.CTkLabel(
            self.main,
            text="Привіт ❤️ Я готова до розмови.",
            wraplength=400,
            justify="left",
            font=("Segoe UI", 16),
        )
        self.response.pack(padx=20, pady=25)

        self.bottom = ctk.CTkFrame(
            self.root,
            height=60,
            corner_radius=0,
            fg_color="#202225",
        )
        self.bottom.pack(fill="x")

        self.entry = ctk.CTkEntry(
            self.bottom,
            height=40,
            placeholder_text="Напишіть повідомлення...",
            font=("Segoe UI", 14),
            corner_radius=20,
        )
        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 8),
            pady=10,
        )
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            self.bottom,
            text="➤",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#5865F2",
            hover_color="#7289DA",
            command=self.send_message,
        )
        self.send_button.pack(side="right", padx=(0, 5))

        self.translate_button = ctk.CTkButton(
            self.bottom,
            text="🌐",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#5865F2",
            hover_color="#7289DA",
            command=self.window_translator.toggle_translation,
        )
        self.translate_button.pack(side="right", padx=(0, 15))

        self.entry.focus()
        self.update_activity()
        self.update_status()

    def toggle_avatar_menu(self):
        if self.avatar_menu is None:
            self.avatar_menu = AvatarMenu(
                self.root,
                self.window_translator,
            )
            self.avatar_menu.place(relx=1.0, x=-195, y=65)
        else:
            self.avatar_menu.destroy()
            self.avatar_menu = None

    def send_message(self, event=None):
        text = self.entry.get().strip()

        if not text:
            return

        self.entry.delete(0, "end")
        self.update_activity()
        self.start_typing_animation()

        self.root.after(450, lambda: self.generate_answer(text))

    def generate_answer(self, text):
        try:
            response = self.chatbot.get_response(text)
        except Exception as error:
            print(f"❌ Помилка чату: {error}")
            response = "Щось пішло не так 😔 Спробуй ще раз."

        delay = min(500 + len(response) * 15, 4000)
        self.root.after(
            delay,
            lambda: self.stop_typing_animation(response),
        )

    def start_typing_animation(self):
        self.typing_frames = [
            "Ніка друкує .",
            "Ніка друкує ..",
            "Ніка друкує ...",
        ]
        self.current_frame = 0
        self.animate_typing()

    def animate_typing(self):
        self.response.configure(
            text=self.typing_frames[self.current_frame]
        )
        self.current_frame = (
            self.current_frame + 1
        ) % len(self.typing_frames)

        self.typing_job = self.root.after(
            500,
            self.animate_typing,
        )

    def stop_typing_animation(self, response):
        if hasattr(self, "typing_job"):
            try:
                self.root.after_cancel(self.typing_job)
            except Exception:
                pass

        self.response.configure(text=response)

    def update_activity(self):
        self.last_activity = datetime.now()
        self.status.configure(
            text="🟢 Онлайн",
            text_color="#57F287",
        )

    def update_status(self):
        diff = datetime.now() - self.last_activity
        minutes = int(diff.total_seconds() // 60)

        if minutes == 0:
            text = "🟢 Онлайн"
            color = "#57F287"
        elif minutes < 60:
            text = f"⚪ Була {minutes} хв тому"
            color = "#aaaaaa"
        else:
            text = (
                "⚪ Була в мережі о "
                + self.last_activity.strftime("%H:%M")
            )
            color = "#777777"

        self.status.configure(
            text=text,
            text_color=color,
        )
        self.root.after(10000, self.update_status)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatGUI(root)
    root.mainloop()
