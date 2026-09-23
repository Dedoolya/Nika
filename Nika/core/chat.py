from modules.dialogue import Dialogue
from core.memory import Memory
from core.translator import Translator
import traceback


class ChatBot:
    def __init__(self):
        self.bot = Dialogue("data/config.json")
        self.memory = Memory()
        self.translator = Translator()

    def get_response(self, user_input: str) -> str:

        text = user_input.strip()

        # вихід
        if text.lower() in ["вийти", "exit", "quit"]:
            return "До зустрічі, сонечко 🌙"

        # -----------------------------
        # Перекладач
        # -----------------------------

        if text.lower().startswith("переклади "):
            phrase = text[10:].strip()

            if not phrase:
                return "Напиши текст після команди 😊"

            try:
                return self.translator.translate(phrase)
            except Exception:
                return traceback.format_exc()

        if text.lower().startswith("translate "):
            phrase = text[10:].strip()

            if not phrase:
                return "Write text after command 😊"

            try:
                return self.translator.translate(phrase)
            except Exception:
                return traceback.format_exc()

        # -----------------------------
        # Пам'ять
        # -----------------------------

        if text.startswith("запам’ятай "):
            parts = text.split(" ", 2)

            if len(parts) == 3:
                self.memory.save("user", f"{parts[1]}={parts[2]}")
                return "Я запам’ятала 💕"

        if text.startswith("згадай "):
            parts = text.split(" ", 1)

            if len(parts) == 2:
                value = self.memory.recall(parts[1])

                if value:
                    return f"Ти казав: {value}"

                return "Нічого не пам’ятаю про це 🤍"

        # -----------------------------
        # Звичайний чат
        # -----------------------------

        return self.bot.get_response(text)


def run():
    chat = ChatBot()

    print("Бот-дівчина запущений 💖 (напиши 'вийти' щоб завершити)")

    while True:

        user_input = input("Ти: ")

        response = chat.get_response(user_input)

        print("Бот:", response)

        if response == "До зустрічі, сонечко 🌙":
            break


if __name__ == "__main__":
    run()