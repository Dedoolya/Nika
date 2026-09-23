import hashlib
import os
import subprocess
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PATH = os.path.join(BASE_DIR, "venv")
PYTHON_BIN = os.path.join(VENV_PATH, "bin", "python")
PIP_BIN = os.path.join(VENV_PATH, "bin", "pip")
REQUIREMENTS_FILE = os.path.join(BASE_DIR, "requirements.txt")
REQUIREMENTS_HASH_FILE = os.path.join(VENV_PATH, ".requirements.sha256")


def run_command(command, *, cwd=BASE_DIR):
    """Run a command and stop with a useful error if it fails."""
    subprocess.run(command, cwd=cwd, check=True)


def requirements_hash():
    if not os.path.exists(REQUIREMENTS_FILE):
        return None

    with open(REQUIREMENTS_FILE, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()


def dependencies_need_install():
    current_hash = requirements_hash()

    if current_hash is None:
        return False

    if not os.path.exists(REQUIREMENTS_HASH_FILE):
        return True

    with open(REQUIREMENTS_HASH_FILE, "r", encoding="utf-8") as file:
        installed_hash = file.read().strip()

    return installed_hash != current_hash


def install_dependencies():
    if not os.path.exists(REQUIREMENTS_FILE):
        print("⚠️ requirements.txt не знайдено")
        return

    print("📦 Встановлюю залежності...")
    run_command([PIP_BIN, "install", "--upgrade", "pip"])
    run_command([PIP_BIN, "install", "-r", REQUIREMENTS_FILE])

    current_hash = requirements_hash()
    if current_hash:
        with open(REQUIREMENTS_HASH_FILE, "w", encoding="utf-8") as file:
            file.write(current_hash)

    print("✅ Залежності готові")


def ensure_venv():
    if not os.path.exists(PYTHON_BIN):
        print("🔧 Створюю віртуальне середовище...")
        run_command([sys.executable, "-m", "venv", VENV_PATH])

    if dependencies_need_install():
        install_dependencies()

    return PYTHON_BIN


def run_bot():
    python_bin = ensure_venv()

    if len(sys.argv) > 1 and sys.argv[1] in {"install", "--install"}:
        print("✅ Встановлення завершено")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        module = "interface.gui"
    else:
        module = "core.chat"

    print(f"🚀 Запускаю Nika: {module}")
    run_command([python_bin, "-m", module])


if __name__ == "__main__":
    run_bot()
