from core.chat import ChatBot

def run_console():
    bot = ChatBot()
    print("Помічник Ніку готовий. Напишіть повідомлення:")

    while True:
        user_input = input("Ви: ")
        if user_input.lower() in ["вихід", "exit", "quit"]:
            print("Ніку: До зустрічі!")
            break
        elif user_input.lower() in ["історія", "history"]:
            bot.show_history()
        else:
            response = bot.reply(user_input)
            print("Ніку:", response)
