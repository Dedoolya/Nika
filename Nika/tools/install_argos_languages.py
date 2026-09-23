import argostranslate.package


def install_languages():
    print("🔍 Отримую список мовних пакетів...")

    argostranslate.package.update_package_index()

    available_packages = argostranslate.package.get_available_packages()

    needed = [
        ("en", "uk"),
        ("uk", "en"),
    ]

    for from_code, to_code in needed:
        package = next(
            (
                p for p in available_packages
                if p.from_code == from_code and p.to_code == to_code
            ),
            None
        )

        if package is None:
            print(f"❌ Не знайдено пакет {from_code} → {to_code}")
            continue

        print(f"⬇ Завантажую {from_code} → {to_code}...")

        download_path = package.download()

        print("📦 Встановлюю...")

        argostranslate.package.install_from_path(download_path)

        print(f"✅ {from_code} → {to_code} встановлено")


if __name__ == "__main__":
    install_languages()