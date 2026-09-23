from core.memory import Memory
from core.translator import Translator
from core.paths import DATA_DIR
from modules.dialogue import Dialogue


class ChatBot:
    def __init__(self):
        self.bot = Dialogue()
        self.memory = Memory()
        self.translator = Translator()

    def get_response(self, user_input: str) -> str:
        text = user_input.strip()
        lower_text = text.lower()

        if lower_text in {"вийти", "exit", "quit"}:
            return "До зустрічі, сонечко 🌙"

        if lower_text.startswith("переклади "):
            phrase = text[len("переклади "):].strip()

            if not phrase:
                return "Напиши текст після команди 😊"

            try:
                return self.translator.translate(phrase)
            except Exception as error:
                print(f"❌ Помилка перекладу: {error}")
                return "Не вдалося виконати переклад 😔"

        if lower_text.startswith("translate "):
            phrase = text[len("translate "):].strip()

            if not phrase:
                return "Write text after the command 😊"

            try:
                return self.translator.translate(phrase)
            except Exception as error:
                print(f"❌ Translation error: {error}")
                return "Translation failed 😔"

        if text.startswith(("запам’ятай ", "запам'ятай ")):
            parts = text.split(" ", 2)

            if len(parts) == 3:
                self.memory.save("user", f"{parts[1]}={parts[2]}")
                return "Я запам’ятала 💕"

            return "Скажи, що саме мені запам’ятати 😊"

        if text.startswith("згадай "):
            key = text.split(" ", 1)[1].strip()

            if key:
                value = self.memory.recall(key)

                if value is not None:
                    return f"Ти казав: {value}"

                return "Нічого не пам’ятаю про це 🤍"

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
