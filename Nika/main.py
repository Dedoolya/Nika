import os
import sys
import subprocess


def ensure_venv():
    venv_path = os.path.join(os.path.dirname(__file__), "venv")
    python_bin = os.path.join(venv_path, "bin", "python")
    pip_bin = os.path.join(venv_path, "bin", "pip")

    # якщо середовище ще не створене
    if not os.path.exists(venv_path):
        print("🔧 Створюю віртуальне середовище...")
        subprocess.run([sys.executable, "-m", "venv", venv_path])

    # завжди перевіряємо requirements.txt
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_file):
        print("📦 Перевіряю залежності...")
        subprocess.run([pip_bin, "install", "--upgrade", "pip"])
        subprocess.run([pip_bin, "install", "-r", req_file])
        print("✅ Усі пакети встановлені")

    return python_bin

def run_bot():
    python_bin = ensure_venv()
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        subprocess.run([python_bin, "-m", "interface.gui"])
    else:
        subprocess.run([python_bin, "-m", "core.chat"])

if __name__ == "__main__":
    run_bot()
