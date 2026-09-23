import customtkinter as ctk


class Overlay:
    def __init__(self, root):
        self.root = root
        self.labels = []

        # невелике зміщення для точнішого попадання
        self.offset_x = 0
        self.offset_y = 4

        # кольори як у ChatGUI
        self.bg_color = "#18191c"       # фон вікна
        self.frame_color = "#202225"    # фон контейнера
        self.border_color = "#5865F2"   # колір рамки

        # шрифт
        self.font = ("Segoe UI", 16, "bold")

    def clear(self):
        for win in self.labels:
            try:
                win.destroy()
            except Exception:
                pass
        self.labels.clear()

    def hide(self):
        self.clear()

    def show_translation(self, x, y, text):
        # створюємо overlay‑вікно
        win = ctk.CTkToplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)

        # контейнер з рамкою
        frame = ctk.CTkFrame(
            win,
            fg_color=self.frame_color,
            corner_radius=7,          # закруглені кути
            border_width=2,            # товщина рамки
            border_color=self.border_color
        )
        frame.pack(padx=2, pady=2)

        # текст перекладу
        label = ctk.CTkLabel(
            frame,
            text=text,
            font=self.font,
            text_color="white",
            wraplength=400,
            justify="center"
        )
        label.pack(padx=10, pady=6)

        win.update_idletasks()

        w = win.winfo_width()
        h = win.winfo_height()

        px = int(x - w / 2 + self.offset_x)
        py = int(y - h / 2 + self.offset_y)

        win.geometry(f"{w}x{h}+{px}+{py}")

        self.labels.append(win)

    def hide_oldest(self):
        if not self.labels:
            return
        try:
            self.labels[0].destroy()
        except Exception:
            pass
        self.labels.pop(0)

    def is_visible(self):
        return len(self.labels) > 0
