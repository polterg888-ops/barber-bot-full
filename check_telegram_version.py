# check_telegram_version.py
import pkg_resources

try:
    version = pkg_resources.get_distribution("python-telegram-bot").version
    print(f"Версия python-telegram-bot: {version}")
    
    if version.startswith("13."):
        print("✅ Правильная версия (13.x)")
    else:
        print(f"❌ Неправильная версия! Нужна 13.x, а у вас {version}")
        print("Установите: pip install python-telegram-bot==13.15")
except Exception as e:
    print(f"Ошибка: {e}")
